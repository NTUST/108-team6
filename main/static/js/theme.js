/**
 * Torbara Sport.AK Template for Joomla, exclusively on Envato Market: http://themeforest.net/user/torbara?ref=torbara
 * @encoding     UTF-8
 * @version      1.0
 * @copyright    Copyright (C) 2015 Torbara (http://torbara.com). All rights reserved.
 * @license      GNU General Public License version 2 or later, see http://www.gnu.org/licenses/gpl-2.0.html
 * @author       Vadim Kozhukhov (support@torbara.com)
 */
jQuery(function($) {

    var config = $('html').data('config') || {};
    
    // Fix for RTL sliders
    UIkit.on('beforeready.uk.dom', function () {  
        UIkit.$('[data-uk-slideset],[data-uk-slider]').attr('dir', 'ltr');  
    });

    
   jQuery('.our-team-wrap .team-read-more').click(function(){
       jQuery(this).parent().parent().find('.additional').slideToggle();
       return false;
   });

});

jQuery(window).load(function(){
    
    jQuery('.preloader').fadeOut();
    
});