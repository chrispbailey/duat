/*
 * Generate a screenshot of a file specified by first argument, output to sencond argument
 */
var page    = require('webpage').create();
var fs      = require("fs");
var system  = require("system");

// read contents of page from file
var html = fs.read(system.args[1]);

page.viewportSize = {width: 1280, height: 1024};
page.content = html;

// wait until the content has loaded
page.onLoadFinished = function(status) {
    // save output file
    page.render(system.args[2]);
    phantom.exit();
};
