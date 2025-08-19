const FallbackUsers = [
  { id:1, name:"Rozenny Valentín", email:"rozenny@example.com", password:"123456", accountNumber:"**** 2218", balance:7250, ccLimit:4200, savings:1800, transactions:[
      {category:"Transferencia", amount:350, note:"A Juan"},
      {category:"Pago", amount:220, note:"Luz"},
      {category:"Compras Online", amount:129, note:"Tienda"},
      {category:"Tarjeta de Crédito", amount:450, note:"Corte"},
      {category:"Inversión", amount:300, note:"Fondo"}
  ]},
  { id:2, name:"Ana López", email:"ana@example.com", password:"abcd", accountNumber:"**** 9041", balance:3920, ccLimit:2500, savings:950, transactions:[
      {category:"Pago", amount:140, note:"Internet"},
      {category:"Compras Online", amount:90, note:"Suscripción"}
  ]}
];

function setThemeFromStorage(){
  const t = localStorage.getItem('midas-theme');
  if(t==='dark') document.body.classList.add('dark');
}
function toggleTheme(){
  document.body.classList.toggle('dark');
  localStorage.setItem('midas-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
}
function q(id){ return document.getElementById(id); }

document.addEventListener('DOMContentLoaded',()=>{
  setThemeFromStorage();
  const year = q('year'); if(year) year.textContent = new Date().getFullYear();
  const themeToggle = q('themeToggle'); if(themeToggle) themeToggle.addEventListener('click', toggleTheme);

  const loginForm = q('loginForm');
  if(loginForm){
    loginForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const email = q('email').value.trim();
      const password = q('password').value.trim();
      const errorMsg = q('errorMsg');
      try{
        const res = await fetch('data/users.json');
        const data = await res.json();
        const users = data && data.users ? data.users : FallbackUsers;
        const user = users.find(u=>u.email===email && u.password===password);
        if(user){
          localStorage.setItem('midas-user', JSON.stringify(user));
          window.location.href='dashboard.html';
        }else{
          errorMsg.textContent = 'Credenciales inválidas';
        }
      }catch{
        const user = FallbackUsers.find(u=>u.email===email && u.password===password);
        if(user){
          localStorage.setItem('midas-user', JSON.stringify(user));
          window.location.href='dashboard.html';
        }else{
          errorMsg.textContent = 'Credenciales inválidas';
        }
      }
    });
    const forgot = q('forgotPassword');
    if(forgot){ forgot.addEventListener('click', ()=> alert('Recuperación simulada: contacte soporte de Midas.')); }
  }

  const logoutBtn = q('logoutBtn');
  if(logoutBtn){
    if(!localStorage.getItem('midas-user')) { window.location.href='login.html'; return; }
    logoutBtn.addEventListener('click', ()=>{
      localStorage.removeItem('midas-user');
      window.location.href='login.html';
    });
  }

  const welcome = q('welcomeName');
  const balanceEl = q('balance');
  const acctEl = q('acctNumber');
  const ccLimitEl = q('ccLimit');
  const savingsEl = q('savings');
  const txList = q('transactionsList');

  if(welcome || balanceEl || txList){
    const stored = localStorage.getItem('midas-user');
    if(!stored){ window.location.href='login.html'; return; }
    const user = JSON.parse(stored);
    welcome.textContent = 'Bienvenido, ' + user.name;
    balanceEl.textContent = '$' + user.balance.toLocaleString();
    acctEl.textContent = user.accountNumber || '**** 0000';
    ccLimitEl.textContent = '$' + (user.ccLimit||0).toLocaleString();
    savingsEl.textContent = '$' + (user.savings||0).toLocaleString();
    renderTransactions(user.transactions||[]);
    window.__midasUser = user;
    if(document.getElementById('expenseChart')) window.initExpenseChart(user.transactions||[]);
  }

  function renderTransactions(items){
    if(!txList) return;
    txList.innerHTML = '';
    items.slice().reverse().forEach(t=>{
      const li = document.createElement('li');
      li.className = 'flex items-center justify-between p-3 rounded-lg bg-white/70 dark:bg-gray-800/70';
      li.innerHTML = `<span class="text-sm">${t.category}${t.note ? ' — '+t.note:''}</span><span class="font-semibold">$${t.amount.toLocaleString()}</span>`;
      txList.appendChild(li);
    });
  }

  const navButtons = document.querySelectorAll('.nav-link');
  if(navButtons.length){
    navButtons.forEach(b=> b.addEventListener('click', ()=>{
      navButtons.forEach(x=>x.classList.remove('active'));
      b.classList.add('active');
      const target = b.dataset.section;
      document.querySelectorAll('.section').forEach(s=> s.classList.add('hidden'));
      document.getElementById('section-'+target).classList.remove('hidden');
    }));
  }

  document.querySelectorAll('[data-action]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const action = btn.dataset.action;
      const stored = JSON.parse(localStorage.getItem('midas-user'));
      if(!stored) return;
      const amount = parseFloat(prompt('Monto a procesar:'));
      if(isNaN(amount) || amount<=0) return alert('Monto inválido');
      if(action==='deposit'){
        stored.balance += amount;
        stored.transactions.push({category:'Depósito', amount, note:'Depósito manual'});
      }else if(action==='transfer'){
        if(stored.balance < amount) return alert('Fondos insuficientes');
        stored.balance -= amount;
        stored.transactions.push({category:'Transferencia', amount, note:'Transferencia simulada'});
      }else if(action==='pay'){
        if(stored.balance < amount) return alert('Fondos insuficientes');
        stored.balance -= amount;
        stored.transactions.push({category:'Pago', amount, note:'Pago de servicio'});
      }
      localStorage.setItem('midas-user', JSON.stringify(stored));
      if(balanceEl) balanceEl.textContent = '$' + stored.balance.toLocaleString();
      if(txList) renderTransactions(stored.transactions);
      if(window.updateExpenseChart) window.updateExpenseChart(stored.transactions);
      const accountCards = document.querySelectorAll('.account-card'); accountCards.forEach(c=>{c.classList.add('ring'); setTimeout(()=>c.classList.remove('ring'),350);});
    });
  });
});
