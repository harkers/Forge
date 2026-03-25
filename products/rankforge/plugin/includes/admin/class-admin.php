<?php
namespace RankForge\Admin;

if (!defined('ABSPATH')) exit;

class Admin {
    public static function init() {
        add_action('admin_menu', [__CLASS__, 'register_menu']);
    }

    public static function register_menu() {
        add_menu_page(
            'RankForge',
            'RankForge',
            'manage_options',
            'rankforge-dashboard',
            [__CLASS__, 'render_dashboard'],
            'dashicons-chart-area',
            58
        );
    }

    public static function render_dashboard() {
        require plugin_dir_path(__FILE__) . 'views/dashboard.php';
    }
}
