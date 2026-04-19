(function () {
  // Split a label onto two lines at the whitespace boundary that best balances
  // the two line lengths, preserving word order. Returns a string (single line)
  // or array of strings (multi-line, as Chart.js expects).
  function wrapLabel(label, maxLen) {
    if (!label || label.length <= maxLen) return label;
    var words = label.split(/\s+/);
    if (words.length === 1) return label;
    var bestSplit = 1;
    var bestDiff = Infinity;
    for (var s = 1; s < words.length; s++) {
      var a = words.slice(0, s).join(' ').length;
      var b = words.slice(s).join(' ').length;
      var diff = Math.abs(a - b);
      if (diff < bestDiff) { bestDiff = diff; bestSplit = s; }
    }
    return [words.slice(0, bestSplit).join(' '), words.slice(bestSplit).join(' ')];
  }

  function init() {
    var canvas = document.getElementById('radar-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    var axes;
    try { axes = JSON.parse(canvas.dataset.axes || '[]'); } catch (e) { axes = []; }
    if (!axes.length) return;

    function themeColors() {
      var styles = getComputedStyle(document.documentElement);
      return {
        accent: styles.getPropertyValue('--accent').trim() || '#1f6feb',
        grid:   styles.getPropertyValue('--border').trim() || '#e3e4e8',
        text:   styles.getPropertyValue('--fg-muted').trim() || '#4a4f5a'
      };
    }

    var colors = themeColors();

    var chart = new Chart(canvas, {
      type: 'radar',
      data: {
        labels: axes.map(function (a) { return a.label; }),
        datasets: [{
          label: 'Proficiency',
          data: axes.map(function (a) { return a.value; }),
          backgroundColor: colors.accent + '33',
          borderColor: colors.accent,
          borderWidth: 2,
          pointBackgroundColor: colors.accent,
          pointRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        layout: {
          // Extra room around the polygon so wrapped labels never touch the canvas edge.
          padding: { top: 16, right: 24, bottom: 16, left: 24 }
        },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (ctx) { return ctx.parsed.r + ' / 100'; } } }
        },
        scales: {
          r: {
            min: 0, max: 100,
            ticks: { display: false, stepSize: 25 },
            grid:       { color: colors.grid },
            angleLines: { color: colors.grid },
            pointLabels: {
              color: colors.text,
              font: { size: 12, weight: '500' },
              padding: 8,
              centerPointLabels: false,
              callback: function (label) { return wrapLabel(label, 16); }
            }
          }
        }
      }
    });

    // Rebuild colors when theme changes
    var observer = new MutationObserver(function () {
      var c = themeColors();
      chart.data.datasets[0].backgroundColor = c.accent + '33';
      chart.data.datasets[0].borderColor = c.accent;
      chart.data.datasets[0].pointBackgroundColor = c.accent;
      chart.options.scales.r.grid.color = c.grid;
      chart.options.scales.r.angleLines.color = c.grid;
      chart.options.scales.r.pointLabels.color = c.text;
      chart.update('none');
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
