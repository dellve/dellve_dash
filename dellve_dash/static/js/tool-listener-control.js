/*
 * Javascript handlers for
 *        1. intiating start/stop requests to Dellve Api
 *        2. long polling Dellve API for tool run progress
 *        3. updating tool listensrs
 *            -start/stop button
 *            -config editor
 *            -progress bar
 *            -run detail heading and log
 *
 * Author: Abigail Johnson
 */

// Use long-poll progress proxy to access cross origin resource
function PollRequest(server_ip, dellve_port) {
  this.pollTimer = null;
  this.interval = 1000; // Request benchmark progress every second
  this.url = '/progress-proxy?url_base=' + server_ip + ':' + dellve_port;
}

// Long poll dellve server for progress updates on currently running benchmark
PollRequest.prototype.activatePoll = function () {
  this.pollTimer = setInterval(() => {
    $.getJSON(this.url, function(runDetail) {
        // Repaint start/stop, run detail logging, and progress bar on tool run updates
        updateControlPanel(runDetail);
        updateProgressBar(runDetail);
        updateRunDetail(runDetail);
    })
  }, this.interval);
};

/* Helper method to update tool start/stop button and dropdown w/ respect to tool run progress */
var firstCheck = true;
function updateControlPanel(runDetail) {
    var activeTool = document.getElementById('benchmark-container');
    var controlButton = document.getElementById('benchmark-start-stop');
    // 1. Init Dropdown to last run on initial page load and init tool config editor
    if (firstCheck == true) {
        firstCheck = false;
        activeTool.value = runDetail['id'];
        updateConfigEditor();
    }
    // 2. Tool Run in Progress
    if ( runDetail['running'] == true  ) {
        activeTool.value = runDetail['id'] // Default dropdown to currently currently running benchmark
        controlButton.className = 'btn btn-warning btn-lg';
        controlButton.value = 'Stop';
    // 3. Tool Run complete or Stopped
    } else {
        controlButton.className = 'btn btn-info btn-lg';
        controlButton.value = 'Start';
    }
}

/* Helper function update progress bar */
function updateProgressBar(runDetail) {
    $('#benchmark-progress').attr('aria-valuenow', runDetail['progress']).css('width',runDetail['progress'] + "%");
    var progressBar = document.getElementById('benchmark-progress');
    // 1. Tool run complete
    if ( runDetail['progress'] == 100 ) {
        progressBar.className = 'progress-bar progress-bar-success progress-bar-striped';
        progressBar.innerHTML = "Complete";
    // 2. Tool run in progress
    } else if ( runDetail['running'] == true ) {
        progressBar.className = 'progress-bar progress-bar-info progress-bar-striped';
        progressBar.innerHTML = runDetail['progress'] + "%";
    // 3. Tool Run stopped
    } else {
        progressBar.className = 'progress-bar progress-bar-warning progress-bar-striped';
        progressBar.innerHTML = 'Stopped';
    }
}

/* Helper method to update Run Detail panel logging and header */
function updateRunDetail(runDetail) {
    // 1. Update Header
    document.getElementById('run-detail-heading').innerHTML = 'Run Detail: ' + runDetail['name'];
    // 2. Update Logging
    var logs = JSON.stringify(runDetail['output']);
    // Remove ANSI codes and misformed literals and styled header
    logs = logs.replace(/['"]+/g, '').replace(/,/g , ' ').replace(/\\n/g, "<br>").replace(/\\t/g, "&nbsp;").replace(/\\u001b\[0m/g, "&nbsp;").replace(/\\u001b\[0;31m/g, "&nbsp;");
    logs = logs.substring(1, logs.length-1);
    var header = "";
    if (runDetail['name']!= 'HPL') {
        header = "<p id='log-header' style='text-align:center'>====================================================================================<br><br>";
        header = header += runDetail['name'] += "<br>Dellve Deep GPU Stress and Benchmark Tool Suite<br>The University of Texas at Austin ECE<br>Senior Design Spring 2017<br><br>";
        header =  header += "Quinito Baula, Travis Chau, Abigail Johnson, Jayesh Joshi, Konstantyn Komarov<br><br>";
        header = header += "====================================================================================<br><br></p>";
    }
    document.getElementById('run-detail').innerHTML = header += logs;
    // 3. Default scroll to bottom on active tool run
    if ( runDetail['running'] == true ) {
        document.getElementById('run-detail').scrollTop = document.getElementById('run-detail').scrollHeight;
    }
}

/* Helper method repaint tool config editor on dropdown tool change schema validation */
updateConfigEditor();
function updateConfigEditor() {
    var elem = document.getElementById("benchmark-container");
    var configStr = elem.options[elem.selectedIndex].getAttribute('data-config');
    var schemaStr = elem.options[elem.selectedIndex].getAttribute('data-schema');
    configStr = configStr.replace(/'/g, '"');
    schemaStr = schemaStr.replace(/'/g, '"');
    var updatedConfig = JSON.parse(configStr);
    var schema = JSON.parse(schemaStr);

    container = document.getElementById("config-editor");
    container.innerHTML = '';
    configEditor = new JSONEditor(container, {
        mode: 'form',
        name: 'Configuration Options',
        search: false,
        schema: schema
    });
    configEditor.set(updatedConfig);
    $( ".jsoneditor-menu" ).remove();
    $( ".jsoneditor-schema-error" ).css('color', '#FFFFFF');
    $( ".jsoneditor-popover jsoneditor-left" ).innerHTML = "Contains invalid parameters. Default config file will be used if submitted.";
    $( ".jsoneditor-tree" ).css('background-color', '#FFFFFF');
    $( ".jsoneditor-separator" ).css('background', '#FFFFFF');
    $( ".jsoneditor-mode-form").css('border', 0);
    //configEditor.enable();
}

/*   Action handler for stop/start commands */
function getToolAction(server_ip, dellve_port) {
    // 1. Send start/stop to DellveAPI
    var benchmarkId = document.getElementById('benchmark-container').value;
    var controlButton = document.getElementById('benchmark-start-stop');
    $.ajax({
      type: "POST",
      url: '/tool-action-proxy?b_id=' + benchmarkId + '&url_base=' + server_ip + ':' + dellve_port + '&action=' + controlButton.value,
      data: JSON.stringify(configEditor.get()),
      success: function(){},
      dataType: "json",
      contentType : "application/json"
    });
    //2 .Repaint Buttons
    // Benchmark Start
    if ( controlButton.value == 'Start') {
        document.getElementById('run-detail').innerHTML = ''; // clear logs
        $('#benchmark-progress').attr('aria-valuenow', 0).css('width', "0%"); // reset progress
        document.getElementById('benchmark-progress').innerHTML = "0 %";
        controlButton.value = 'Stop';
        controlButton.className = 'btn btn-warning btn-lg';
        document.getElementById('benchmark-progress').className = 'progress-bar progress-bar-info progress-bar-striped';
    // Benchmark stop
    } else {
        controlButton.value = 'Start';
        controlButton.className = 'btn btn-info btn-lg';
        document.getElementById('benchmark-progress').className = 'progress-bar progress-bar-warning progress-bar-striped';
        document.getElementById('benchmark-progress').innerHTML = 'Stopped';
    }
}

/* Exports most recent tool run detail as pdf
TODO: format export */
$(function () {
  $('#export-report-button').click(function () {
    var doc = new jsPDF();
    doc.setFontSize(12);
    doc.setTextColor(0);
    doc.setDrawColor(0,0,0);

    // Add page content
    var content = document.getElementById('run-detail').innerHTML;
    content = content.substring(content.indexOf(">") + 1);
    //content = content.substring(content.indexOf(">") + 1);
    //content = content.replace(/<br>/g, "\n");
    var lines = content.split('<br>');
    console.log('lines:' + lines.length);
    var cutoff = 50; // num lines till next page break

    for ( i = 0; i < lines.length; i += cutoff ) {
        var pageContent = lines.slice(i, i + cutoff );
        doc.text(20,30, pageContent );
        if (i + cutoff <= lines.length) {
            doc.addPage();
        }
    }

    // Save File
    var fileName = 'dellve_run_' + Date().toLocaleString() + '.pdf';
    doc.save(fileName);
    });
});
