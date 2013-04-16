(function() {

    window.Feedback = {}

    window.Feedback.enabled = false;
    
    window.Feedback.init = function(){
        // load css
        var filename = '//{{host}}{{STATIC_URL}}css/feedback.css';
        var fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", filename);
        document.getElementsByTagName("head")[0].appendChild(fileref);
        
        var str = "<div class='feedback_window feedback_ignore'>"+
        "<button class='feedback-btn feedback_start' onclick='window.Feedback.show_form()'>Send Feedback</button>"+
        "<div class='feedback_extra' style='display:none;'>"+
            "<div class='feedback_top'>"+
                "<div class='feedback_sending'><p>Sending...</p><img src='//{{host}}{{STATIC_URL}}/images/ajax-loader.gif'/></div>"+
                "<div class='feedback_success'><p>Submission sent successfully!</p></div>"+
                "<div class='feedback_failure'><p>Submission failed!</p></div>"+
                "<div class='feedback_form'>"+
                    "<p>Please describe the issue you are experiencing:</p>"+
                    "<textarea name='comment'></textarea>"+
                "</div>"+
            "</div>"+
            "<div class='feedback_actions'>"+
                "<button class='feedback-btn feedback_send' onclick='window.Feedback.submit()'>Send</button>"+
                "<button class='feedback-btn' onclick='window.Feedback.reset()'>Cancel</button>"+
            "</div>"+
        "</div>"+
        "</div>";
        jQuery("body").append(str);
        jQuery(".feedback_window *").addClass("feedback_ignore");
    };

    window.Feedback.show_form = function (){
        jQuery('.feedback_send').removeAttr('disabled');
        jQuery('.feedback_sending').hide();
        jQuery('.feedback_success').hide();
        jQuery('.feedback_failure').hide();
        jQuery('.feedback_form').show();

        jQuery('.feedback_window .feedback_extra').slideDown();
        window.Feedback.enable_selection();
        jQuery('.feedback_window .feedback_start').fadeOut();
    };

    window.Feedback.lastelem = null;

    window.Feedback.enable_selection = function(){
        window.Feedback.enabled = true;
        
        jQuery("body *:not(.feedback_ignore)").addClass("feedback_unselected");
        
        document.onmouseover = function(e) {
            var event = e || window.event;

            if (window.Feedback.lastelem) {
                jQuery("*", window.Feedback.lastelem).removeClass("feedback_hover");
                jQuery(window.Feedback.lastelem).removeClass("feedback_hover");
            }

            var target = event.target || event.srcElement;
            
            if (target != document.body && !jQuery(target).hasClass('feedback_ignore')) {
                jQuery(target).addClass("feedback_hover");
            }
            window.Feedback.lastelem = target;
        };
        
        document.onclick = function(event) {
            if (window.Feedback.enabled) {
                var target = event.target || event.srcElement;
                if (!jQuery(target).hasClass('feedback_ignore')) {
                    jQuery(target).toggleClass("feedback_selected");
                }
                event.preventDefault();
                event.stopPropagation();
                return false;
            }
        };
    }; // END enable_selection()

    window.Feedback.submit = function(){
        // send
        var url = '//{{host}}/project/bos2/submit';
        var data = {};
        // add extra useful information
        data['url'] = window.location.href;
        data['referrer'] = document.referrer;
        data['comment'] = jQuery('.feedback_form textarea').val();
        
        // hide feedback while we take a snapshot..
        jQuery('.feedback_window').hide();
        var page = document.documentElement.outerHTML;
        jQuery('.feedback_window').show();
        data['html'] = page;
        window.Feedback.send(url, data);
        
        window.Feedback.show_loading();
    }; // END submit()

    window.Feedback.reset = function(){
        // reset page
        window.Feedback.enabled = false;
        jQuery('.feedback_window .feedback_start').fadeIn();
        jQuery('.feedback_form textarea').val("");
        jQuery('.feedback_window .feedback_extra').slideUp();
        jQuery("body *").removeClass('feedback_unselected');
        jQuery("body *").removeClass('feedback_selected');
        jQuery("body *").removeClass('feedback_hover');
        document.onmouseover = document.click = null;
    };

    window.Feedback.show_loading = function() {
        jQuery('.feedback_failure').hide();
        jQuery('.feedback_success').hide();
        jQuery('.feedback_form').slideUp('fast');
        jQuery('.feedback_sending').slideDown('fast');
    }
    
    window.Feedback.success = function()
    {
        jQuery('.feedback_sending').slideUp('fast');
        jQuery('.feedback_success').slideDown('fast');
        window.setTimeout(function(){window.Feedback.reset()},2000);
    }

    window.Feedback.failure = function()
    {
        jQuery('.feedback_sending').slideUp('fast');
        jQuery('.feedback_failure').slideDown('fast');
    }

    window.Feedback.send = function( url, data ) {
    
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if( xhr.readyState == 4 && xhr.status === 200) {
                window.Feedback.success();
            }
            if( xhr.readyState == 4 && xhr.status !== 200) {
                window.Feedback.failure();
            }
        };

        xhr.open( "POST", url, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send( "data=" + encodeURIComponent( window.JSON.stringify( data ) ) );
        
    };
    
    // Insert a script into the current document and run callback when loaded
    window.Feedback.getScript = function(url, success) {
        var script = document.createElement('script');
        script.src = url;

        var head = document.getElementsByTagName('head')[0], done = false;

        // Attach handlers for all browsers
        script.onload = script.onreadystatechange = function() {

            if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete'))
            {
                done = true;

                // callback function provided as param
                success();
                script.onload = script.onreadystatechange = null;
                head.removeChild(script);
            };
        };
        head.appendChild(script);
    };


    // Load jquery if missing
    // http://css-tricks.com/snippets/jquery/load-jquery-only-if-not-present/
    // Only do anything if jQuery isn't defined
    if (typeof jQuery == 'undefined') {
        window.Feedback.getScript('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', function() {

            if (typeof jQuery == 'undefined') {
                // Super failsafe - still somehow failed...
            } else {
                // jQuery loaded! Make sure to use .noConflict just in case
                jQuery(document).ready(window.Feedback.init);
                jQuery.noConflict();
            }
        });
    } else { // jQuery was already loaded
        jQuery(document).ready(window.Feedback.init);
    };


})();
