var fs = require('fs');
var utils = require('utils');
var casper = require('casper').create({
  verbose: true,
  logLevel: 'debug',
  pageSettings: {
    loadImages: false,
    loadPlugins: false,
    userAgent: 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36'
  }
});
/*
 *
 * Can be remade by
 *  - visting https://acquia.mavenlink.com/users/5989367-sean-hamlin/dashboard?tab=projects&filter=account
 *  - running javascript on each page
 *

var projects = [];
jQuery('.tbl-row').each( function( index, element ){
  projects.push({
    'name': $.trim($(this).find('.workspace-title').text()),
    'id': $(this).data('workspace-id'),
  })
});
console.log(JSON.stringify(projects));
*/

var accounts = [];

function getStartDate() {
  var d = new Date();
  var month = '' + (d.getMonth() + 1);
  var day = '01';
  var year = d.getFullYear();

  if (month.length < 2) month = '0' + month;

  return [year, month, day].join('-');
}
function getEndDate() {
  var today = new Date();
  var d = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  var month = '' + (d.getMonth() + 1);
  var day = '' + d.getDate();
  var year = d.getFullYear();

  if (month.length < 2) month = '0' + month;
  if (day.length < 2) day = '0' + day;

  return [year, month, day].join('-');
}

casper.start('https://acquia.mavenlink.com/reports/insights/31837', function () {
 this.fillSelectors('form#openid-form', {
    'input[name="login[email_address]"]' : casper.cli.get("username"),
    'input[name="login[password]"]' : casper.cli.get("password")
  }, true);
});

casper.then(function() {
  this.echo(this.getTitle());
});

var count = 0;
casper.repeat(accounts.length, function() {
  var thisAccount = accounts[count++];
  require('utils').dump(thisAccount);

  casper.thenOpen('https://acquia.mavenlink.com/reports/time_tracking/grouped?organizations=%3B&group_id=&workspace_id=' + thisAccount.id + '&hours_range_min=&hours_range_max=&start_date=' + getStartDate() + '&end_date=' + getEndDate() + '&creator_id=&invoice_status=all&story_id=&story_type=all&group_type=submitter&role_ids=', function (response) {
    var accountJson = JSON.parse(this.evaluate(function() {
      return document.body.textContent || document.body.innerText;
    }));
    var index = count - 1;
    accounts[index].billable = accountJson['overview']['total_billable_minutes'];
    accounts[index].nonbillable = accountJson['overview']['total_non_billable_minutes'];
  });
});

casper.run(function () {
  fs.remove('accounts.json');
  fs.write('accounts.json', JSON.stringify(accounts), 'w');
  this.echo("Accounts CSV written");
  this.exit();
});
