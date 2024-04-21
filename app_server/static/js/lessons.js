// courseID from script tag in courses.html

$('div.tab-content').each(function () {
    let $tabContent = $(this);
    let lessonNUM = $tabContent.attr('id');
    let myURL = "http://localhost:5000/course/" + courseID + "/lesson/" + lessonNUM;
    $.ajax({
        method: 'GET',
        url: myURL
    })
        .done(function (data) {
            $tabContent.html(data);
            console.log(data)
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX request failed:', errorThrown);
            $tabContent.html("<h1>Something went wrong!...</h1>");
        });
})

