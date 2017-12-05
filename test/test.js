var page = require('webpage').create();
page.open('https://www.youtube.com/user/PhoneBunch/about', function(status) {
  console.log("Status: " + status);
  if(status === "success") {
    page.render('example.png');
  }
  phantom.exit();
});