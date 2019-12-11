$(document).ready(function () {
  var pros_wc_data = $('#pros-word-cloud-data').data("content");
  var cons_wc_data = $('#cons-word-cloud-data').data("content");
  $('#pros_word_cloud').jQCloud(pros_wc_data, {
     autoResize: true
  });
  $('#cons_word_cloud').jQCloud(cons_wc_data, {
     autoResize: true
  });
   
});