import { chromium } from '@playwright/test';
import fs from 'node:fs';

let onboarded = false;
const user = {
  id: 'preview-user', email: 'preview@cvln.test', display_name: 'Preview Academy',
  frek_id: 'FREK-PREVIEW-001', role: 'student', onboarding_completed: false,
  stade: 'graine', cc_credits: 0, lang: 'fr',
  signals: {'FREK-TIME':0,'FREK-WORK':0,'FREK-SCORE':0,'FREK-LINK':0,'FREK-CERT':0,'FREK-CONTRIB':0}
};
const poles = [
  {code:'FMS',name:'Factory Maker Studio',color:'#E05A33'},
  {code:'KLT',name:'Kiltikonet',color:'#143628'},
  {code:'KOR',name:'KORA',color:'#F59E0B'},
  {code:'FRK',name:'FREK',color:'#C2410C'}
];
const formations = [
  {code:'FMS-A',name:'Artist Development',pole:'FMS',pole_color:'#E05A33',duration_h:12,cc:40,modules_count:8,validated_count:0,progress_pct:0,is_recommended:true,is_unlocked:true},
  {code:'FMS-B',name:'Music Business',pole:'FMS',pole_color:'#E05A33',duration_h:10,cc:35,modules_count:6,validated_count:0,progress_pct:0,is_recommended:true,is_unlocked:true},
  {code:'KLT-01',name:'Réseau culturel',pole:'KLT',pole_color:'#143628',duration_h:10,cc:30,modules_count:6,validated_count:0,progress_pct:0,is_recommended:false,is_unlocked:true}
];
const missions = [{code:'MIS-001',pole:'FMS',entity:'Factory Maker Studio',title:'Définir ton positionnement artistique',cc_reward:10,description:'Preview',stade_min:'graine',featured:true,urgent:false}];
const badge = {code:'BADGE-DECOUVERTE',name:'Découverte',tier:'Graine',cc_threshold:0,description:'Premiers pas dans CVLN Academy.',color:'#A37D62'};
const path = () => ({metier_vise:'FMS',own_pole:formations.slice(0,2),other_poles:formations.slice(2),canonical:{canonical_formations:[]},next_action:{formation_code:'FMS-A',formation_name:'Artist Development',module_code:'FMS-A-M01',module_name:'Construire ton identité artistique',status:'available',pole_color:'#E05A33',route:'/formations/FMS-A/modules/FMS-A-M01',resume:false}});

function payload(method, p, body={}) {
  if (p==='/auth/me') return user;
  if (p==='/auth/register' || p==='/auth/login') { if (p==='/auth/register') { user.display_name=body.display_name||user.display_name; user.email=body.email||user.email; } return {token:'preview-token',refresh_token:'preview-refresh',user}; }
  if (p==='/auth/refresh') return {token:'preview-token',refresh_token:'preview-refresh'};
  if (p==='/auth/logout') return {ok:true};
  if (p==='/onboarding/options') return {langs:['fr','en','kr','es'],metiers:poles,territoires:[{code:'MQ',name:'Martinique'},{code:'GP',name:'Guadeloupe'},{code:'GF',name:'Guyane'},{code:'DIASPORA',name:'Diaspora'}]};
  if (p==='/onboarding/complete') { onboarded=true; user.onboarding_completed=true; return {signals_emitted:['FREK-TIME'],badge_earned:badge,recommended_formation:formations[0],recommended_mission:missions[0]}; }
  if (p==='/poles') return poles;
  if (p==='/formations') return formations;
  if (p==='/user/learning-path') return path();
  if (p==='/progression/summary') return {global_pct:0,completed_modules:0,total_modules:24,canonical:{canonical_modules_total:0,canonical_modules_viewed:0,canonical_progress_pct:0}};
  if (p==='/progression/horizon') return [];
  if (p==='/frek/profile') return {stade_progress_pct:0,stade_next_at:10,returning:false,recent_signals:[],canonical:{canonical_modules_total:0}};
  if (p==='/missions') return missions;
  if (p==='/missions/mine') return [];
  if (p==='/badges/mine') return onboarded ? [badge] : [];
  if (p==='/badges') return [badge];
  if (p==='/wallet/me') return {account:{jcc_balance:0,token_balance:0,badges:[]},recent_transactions:[]};
  if (p==='/skills/mine' || p==='/qualifications/mine' || p==='/certifications/attempts/mine' || p==='/certifications/rubrics' || p==='/commerce/offers') return [];
  if (p==='/professional/profile/mine') return {is_public:false,acquired_skills:[],certifications:[]};
  if (p==='/ecosystem-builder/me') return {stage:'learner',portfolio:[],credentials:[],verified_proofs:[],missions_completed:[],ecosystem_history:[]};
  if (method!=='GET') return {ok:true};
  return [];
}

const browser = await chromium.launch({headless:true});
const page = await browser.newPage({viewport:{width:1440,height:1000}});
const pageErrors=[];
page.on('pageerror', e => pageErrors.push(String(e)));
await page.route('**/api/**', async route => {
  const req=route.request();
  const u=new URL(req.url());
  let body={}; try { body=req.postDataJSON()||{}; } catch {}
  await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(payload(req.method(),u.pathname.replace(/^\/api/,''),body))});
});
await page.goto('http://127.0.0.1:4173/', {waitUntil:'networkidle'});
await page.getByTestId('landing-page').waitFor();
await page.screenshot({path:'preview-output/01-landing.png',fullPage:true});

await page.getByTestId('auth-display-name').fill('Laurent Preview');
await page.getByTestId('auth-email').fill('laurent.preview@cvln.test');
await page.getByTestId('auth-password').fill('Preview123!');
await page.getByTestId('auth-submit').click();
await page.waitForURL('**/onboarding');
await page.screenshot({path:'preview-output/02-onboarding.png',fullPage:true});
await page.getByTestId('ob-lang-fr').click(); await page.getByTestId('onboarding-next').click();
await page.getByTestId('ob-metier-FMS').click(); await page.getByTestId('onboarding-next').click();
await page.getByTestId('ob-terr-MQ').click(); await page.getByTestId('onboarding-next').click();
await page.getByTestId('ob-objectif').fill('Tester le parcours CVLN Academy'); await page.getByTestId('onboarding-next').click();
await page.getByTestId('onboarding-submit').click();
await page.waitForURL('**/dashboard');
await page.getByTestId('dashboard-page').waitFor();
await page.screenshot({path:'preview-output/03-dashboard.png',fullPage:true});

await page.getByTestId('nav-formations').click();
await page.waitForURL('**/formations');
await page.getByTestId('formations-page').waitFor();
await page.screenshot({path:'preview-output/04-formations.png',fullPage:true});

await page.getByTestId('nav-roadmap').click();
await page.waitForURL('**/roadmap');
await page.getByTestId('roadmap-page').waitFor();
await page.screenshot({path:'preview-output/05-roadmap.png',fullPage:true});

fs.writeFileSync('preview-output/RESULT.json', JSON.stringify({landing:true,onboarding:true,dashboard:true,formations:true,roadmap:true,pageErrors}, null, 2));
if (pageErrors.length) { console.error(pageErrors); process.exitCode=1; }
await browser.close();
