function publish(content_id)
{
    let url = '/api/v1/post/1/edition/'+ content_id +'/set_published/'
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false )
    xmlHttp.send( null );
    return xmlHttp.responseText;
}