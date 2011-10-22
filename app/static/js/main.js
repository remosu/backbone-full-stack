require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'todos'], function() {
    $(document).ready(function() {
        window.App = new TodoApp();
    });
});