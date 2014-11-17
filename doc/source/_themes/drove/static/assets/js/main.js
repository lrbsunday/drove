/*
 * main.js
 * Copyright (C) 2014 ajdiaz <ajdiaz@reineta>
 *
 * Distributed under terms of the MIT license.
 */

$(function() {
$("form.search a").click(function() {
  $("form.search").submit();
});
$("#sidebar-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

/**
   * Patch all tables to remove ``docutils`` class and add Bootstrap base
   * ``table`` class.
   */
  patchTables = function () {
    $("table.docutils")
      .removeClass("docutils")
      .addClass("table")
      .attr("border", 0);
  };

  patchTables();

// Add Note, Warning styles. (BS v2,3 compatible).
    $('.admonition').addClass('alert alert-info')
      .filter('.warning, .caution')
        .removeClass('alert-info')
        .addClass('alert-warning').end()
      .filter('.error, .danger')
        .removeClass('alert-info')
        .addClass('alert-danger alert-error').end();

  $(".section dl dt").each(function(i,o) {
    if ($(o).parent().attr('class') != 'docutils')
      $(o).prepend('<span class="label label-default">' + $(o).parent().attr('class') + '</span>');
  });


});
