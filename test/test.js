var page = require('webpage').create();

phantom.setProxy('proxy.crawlera.com', '8010', 'http'); // change to https when making HTTPS requests
page.customHeaders={'Proxy-Authorization': 'Basic '+btoa('5dba0f67463b4e828e803497d8c1b985:')}; // Make sure to include ':' at the end

page.open('https://www.youtube.com/user/PhoneBunch/about', function(status) {
  console.log("Status: " + status);
  if(status === "success") {
    page.render('example.png');
  }
  phantom.exit();
});