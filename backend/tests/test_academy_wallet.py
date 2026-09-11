import pytest
from pymongo.errors import DuplicateKeyError

from wallet import service


class FakeCursor:
    def __init__(self, docs):
        self.docs = list(docs)

    def sort(self, key, direction):
        reverse = direction < 0
        self.docs.sort(key=lambda d: d.get(key, ""), reverse=reverse)
        return self

    async def to_list(self, limit):
        return self.docs[:limit]

    def __aiter__(self):
        self._iter = iter(self.docs)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class FakeCollection:
    def __init__(self):
        self.docs = []

    async def find_one(self, query, projection=None):
        for doc in self.docs:
            if all(doc.get(k) == v for k, v in query.items()):
                return dict(doc)
        return None

    async def insert_one(self, doc):
        if "effect_key" in doc:
            for existing in self.docs:
                if (
                    existing.get("user_id") == doc.get("user_id")
                    and existing.get("effect_key") == doc.get("effect_key")
                ):
                    raise DuplicateKeyError("duplicate effect")
        if "user_id" in doc and "jcc_balance" in doc:
            for existing in self.docs:
                if existing.get("user_id") == doc.get("user_id"):
                    raise DuplicateKeyError("duplicate account")
        self.docs.append(dict(doc))

    async def update_one(self, query, update):
        doc = await self.find_one(query)
        if doc is None:
            return
        target = next(d for d in self.docs if d.get("user_id") == query.get("user_id"))
        for key, value in update.get("$set", {}).items():
            target[key] = value
        for key, value in update.get("$inc", {}).items():
            target[key] = target.get(key, 0) + value
        for key, value in update.get("$addToSet", {}).items():
            target.setdefault(key, [])
            if value not in target[key]:
                target[key].append(value)

    def find(self, query, projection=None):
        def matches(doc):
            for key, value in query.items():
                if isinstance(value, dict) and "$in" in value:
                    if doc.get(key) not in value["$in"]:
                        return False
                elif doc.get(key) != value:
                    return False
            return True

        docs = [dict(d) for d in self.docs if matches(d)]
        if projection:
            projected = []
            for doc in docs:
                projected.append(
                    {k: v for k, v in doc.items() if projection.get(k) == 1 or k not in projection}
                )
            docs = projected
        return FakeCursor(docs)


class FakeDB:
    def __init__(self):
        self.wallet_accounts = FakeCollection()
        self.wallet_transactions = FakeCollection()


@pytest.mark.asyncio
async def test_same_effect_key_is_applied_once(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr(service, "db", fake_db)

    first = await service.credit(
        "u1",
        "badge_earned",
        10.0,
        effect_key="badge:starter",
        badge_code="starter",
    )
    second = await service.credit(
        "u1",
        "badge_earned",
        10.0,
        effect_key="badge:starter",
        badge_code="starter",
    )

    assert first.id == second.id
    assert len(fake_db.wallet_transactions.docs) == 1
    summary = await service.get_summary("u1")
    assert summary.account.jcc_balance == 10.0
    assert summary.account.badges == ["starter"]


@pytest.mark.asyncio
async def test_summary_repairs_cached_balance_from_history(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr(service, "db", fake_db)

    await service.credit(
        "u2",
        "jcc_earned",
        12.0,
        effect_key="mission:m1",
    )
    fake_db.wallet_accounts.docs[0]["jcc_balance"] = 999.0

    summary = await service.get_summary("u2")

    assert summary.account.jcc_balance == 12.0
    assert fake_db.wallet_accounts.docs[0]["jcc_balance"] == 12.0


@pytest.mark.asyncio
async def test_distinct_effect_keys_allow_distinct_rewards(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr(service, "db", fake_db)

    await service.credit("u3", "jcc_earned", 5.0, effect_key="mission:m1")
    await service.credit("u3", "jcc_earned", 5.0, effect_key="mission:m2")

    summary = await service.get_summary("u3")
    assert summary.account.jcc_balance == 10.0
    assert len(fake_db.wallet_transactions.docs) == 2
