function loadMostRecentBlogPost(selector){
    $.get(
        'http://blog.statsonice.com/comments/feed/',
        function(data) {
            console.log(data);
        },
        'xml'
    );
}
