(function($) {
    var cache = {};
    
    function _render(elt, template, data, callback) {
        var html = template(data);
        elt.html(html);
        callback(html);
    }
    
    /**
     * Fetches the Underscore.js template at the given path,
     * processes it with the provided data object, and finally
     * executes the optional callback.
     */
    $.fn.template = function(path, data, callback) {
        var self = this;
        
        if (cache[path]) {
            _render(self, cache[path], data, callback);
            return self;
        }
        
        $.get(path, function(data) {
            cache[path] = _.template(data);
            _render(self, cache[path], data, callback);
        });
        
        return self;
    };
})(jQuery);