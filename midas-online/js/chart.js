let expenseChart;
function sumByCategory(transactions, category){
  return transactions.filter(t=>t.category===category).reduce((a,b)=>a+(+b.amount||0),0);
}
function buildDataset(transactions){
  const labels = ['Transferencia','Pago','Compras Online','Tarjeta de Crédito','Inversión','Depósito'];
  const data = labels.map(l=> sumByCategory(transactions, l));
  return { labels, data };
}
window.initExpenseChart = function(transactions){
  const ctxEl = document.getElementById('expenseChart'); if(!ctxEl) return;
  const ctx = ctxEl.getContext('2d');
  const gradient = ctx.createLinearGradient(0,0,0,220);
  gradient.addColorStop(0,'rgba(245,197,66,0.95)');
  gradient.addColorStop(1,'rgba(245,197,66,0.35)');
  const ds = buildDataset(transactions);
  if(expenseChart) expenseChart.destroy();
  expenseChart = new Chart(ctx,{
    type:'bar',
    data:{ labels: ds.labels, datasets:[{ label:'Gastos', data: ds.data, backgroundColor: gradient, borderColor:'rgba(212,163,23,1)', borderWidth:1, borderRadius:8 }]},
    options:{
      responsive:true,
      plugins:{ legend:{ display:false }},
      scales:{ y:{ beginAtZero:true }},
      animation:{ duration:900, easing:'easeOutCubic' }
    }
  });
};
window.updateExpenseChart = function(transactions){
  if(!expenseChart) return window.initExpenseChart(transactions);
  const ds = buildDataset(transactions);
  expenseChart.data.labels = ds.labels;
  expenseChart.data.datasets[0].data = ds.data;
  expenseChart.update();
};

  