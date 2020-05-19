let courses = {}
let i = 0;
jQuery('[id*="contentDivImg"]:not([id*="contentDivImg_"])').each(function() {
    let _this = this;
    jQuery(_this).find('tr').each(function(index) {
        let _this_ = this;
        if ( index ) {
            let children = jQuery(_this_).children();
            courses[i] = {};
            courses[i]['title']       = jQuery(_this_).parents('[id*="contentDivImg"]:not([id*="contentDivImg_"])').prev().find('span')[0].innerText;
            courses[i]['class_num']   = children[1].innerText;
            courses[i]['section_num'] = children[2].innerText.substr(0,2);
            courses[i]['day_time']    = children[3].innerText;
            courses[i]['room']        = children[4].innerText;
            courses[i]['instructor']  = children[5].innerText;
            i++;
        }
    });
});
var jsonObject = JSON.stringify(courses);
