<?php
/**
 * Plugin Name: RankForge
 * Description: AI-powered SEO and image optimisation for WordPress
 * Version: 2.6.0
 * Author: sharker
 */

if (!defined('ABSPATH')) exit;

require_once plugin_dir_path(__FILE__) . 'includes/core/class-core.php';

add_action('plugins_loaded', function () {
    \RankForge\Core::init();
});
