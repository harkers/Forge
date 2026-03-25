<?php
namespace RankForge\Core;

if (!defined('ABSPATH')) exit;

class Installer {
    public static function activate() {
        global $wpdb;
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';

        $charset = $wpdb->get_charset_collate();
        $seo = $wpdb->prefix . 'rankforge_seo_queue';
        $img = $wpdb->prefix . 'rankforge_image_queue';

        $sql1 = "CREATE TABLE {$seo} (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT UNSIGNED NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            attempts INT NOT NULL DEFAULT 0,
            last_error LONGTEXT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY post_status (post_id, status)
        ) {$charset};";

        $sql2 = "CREATE TABLE {$img} (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT UNSIGNED NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            attempts INT NOT NULL DEFAULT 0,
            last_error LONGTEXT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY post_status (post_id, status)
        ) {$charset};";

        dbDelta($sql1);
        dbDelta($sql2);
    }
}
