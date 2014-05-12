var page = require('webpage').create();
page.open('http://twitter.com/SchneiderAltuve/status/443869705766330368', function() {
  page.viewportSize = { width: 5000, height: 220 };
  page.clipRect = { top: 46, left: 0, width: 1200, height: 217 };
  page.render('screenshot.png');
  phantom.exit();
});
