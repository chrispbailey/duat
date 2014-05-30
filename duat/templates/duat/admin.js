(function() {

    window.FeedbackAdmin = {}
    
    window.FeedbackAdmin.init = function(){
        // load css
        var filename = '{{STATIC_URL}}duat/css/admin.css';
        var fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", filename);
        document.getElementsByTagName("head")[0].appendChild(fileref);
        
        var str = "<div class='feedback_window '>"+
        "<button class='feedback_toggle' onclick='window.FeedbackAdmin.toggle()'>Toggle highlight</button>"+
        "</div>";
        jQuery("body").append(str);
        
        jQuery('.feedback_selected').addClass('feedback_selected_items');
        
        jQuery('a,button').click(function() {return(false);});
    };

    window.FeedbackAdmin.toggle = function (){
        jQuery('.feedback_selected_items').toggleClass('feedback_selected').toggleClass('feedback_selected_alt');
    };

    // Insert a script into the current document and run callback when loaded
    window.FeedbackAdmin.getScript = function(url, success) {
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
        window.FeedbackAdmin.getScript('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', function() {

            if (typeof jQuery == 'undefined') {
                // Super failsafe - still somehow failed...
            } else {
                // jQuery loaded! Make sure to use .noConflict just in case
                jQuery(document).ready(window.FeedbackAdmin.init);
                jQuery.noConflict();
            }
        });
    } else { // jQuery was already loaded
        jQuery(document).ready(window.FeedbackAdmin.init);
    };

})();