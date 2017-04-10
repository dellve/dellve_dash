//  Netdata config for custom dashboard
// ( This has to be done after dashboard.js is loaded )

// destroy charts not shown (lowers memory on the browser)
NETDATA.options.current.destroy_on_hide = true;
// set this to false, to always show all dimensions
NETDATA.options.current.eliminate_zero_dimensions = true;
// lower the pressure on this browser
NETDATA.options.current.concurrent_refreshes = true;
// if the browser is too slow set this to false
NETDATA.options.current.parallel_refresher = true;
// always update the charts, even if focus is lost
// NETDATA.options.current.stop_updates_when_focus_is_lost = false;

// Servers may become offline for some time, and charts will break.
// This will reload the page every RELOAD_EVERY minutes
//var RELOAD_EVERY = 5;
//setTimeout(function(){
//    location.reload();
//}, RELOAD_EVERY * 60 * 1000);
