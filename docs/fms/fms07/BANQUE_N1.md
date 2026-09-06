# FMS-07 — Banque N1 (formative, M1→M4)

```
Sourced directly against fms-os/fms/backend/server.py (re-read this
session): BookingCreate, ServiceCreate models, /os/bookings,
/os/services routes, and the real 8-state booking status enum.
```

## M1 — session lifecycle

1. Cite les 8 valeurs réelles de statut d'une réservation, dans
   n'importe quel ordre. (`requested`, `pending`, `confirmed`,
   `in_progress`, `completed`, `cancelled`, `rescheduled`, `no_show`)
2. Que se passe-t-il si on envoie un statut hors de cette liste à
   `PATCH /os/bookings/{id}/status` ? (HTTP 400 `"Invalid status"` —
   rejeté par le serveur, jamais silencieusement accepté)
3. Quels champs sont posés automatiquement par le serveur à la
   création d'une réservation, jamais fournis par l'appelant ?
   (`status="confirmed"`, `payment_status="unpaid"`, `id`,
   `created_at`)

## M2 — data model literacy

4. Nomme au moins 5 champs réels du modèle `BookingCreate`.
   (`service_id`, `service_name`, `client_id`, `client_name`,
   `client_email`, `project_id`, `date`, `start_time`, `end_time` —
   toute combinaison de 5)
5. Nomme au moins 5 champs réels du modèle `ServiceCreate`.
   (`name`, `description`, `category`, `duration_hours`, `price`,
   `currency` (défaut `"EUR"`), `location`, `active`, `visible`)
6. Le champ `currency` d'un service a-t-il une valeur par défaut
   réelle ? (Oui — `"EUR"`)

## M3 — coordination de production (bloc FMS-14 absorbé)

7. Explique la différence réelle entre la coordination enseignée dans
   FMS-05 (Artist Management) et celle de ce bloc. (FMS-05 = un Artist
   Manager coordonne la carrière entière d'un artiste ; ce bloc = un
   Production Coordinator coordonne un seul projet studio — budget de
   session, liaison inter-départements pour ce projet, suivi de
   livrables)
8. Ce bloc réutilise-t-il le contenu FMS-05 en le réécrivant ? (Non —
   par référence uniquement, jamais réécrit)

## M4 — booking & resource planning (bloc FMS-16 absorbé)

9. Dans `fms-os/fms`, bookings et services sont-ils gérés par des
   routes séparées ou la même couche `/os` ? (La même couche `/os` —
   c'est la preuve réelle citée pour justifier la fusion de FMS-16
   dans FMS-07 plutôt qu'une formation séparée)
10. Dans quel cas ce corpus recommande-t-il malgré tout un rôle de
    scheduler dédié ? (Dans les opérations plus grandes, où la
    planification se sépare réellement de la gestion de session — un
    cas internal/spécialisation, pas une formation externe parallèle)
