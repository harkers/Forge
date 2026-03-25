<?php
namespace RankForge\Queue;

class SEOQueue {
    public static function table_name() {
        global $wpdb;
        return $wpdb->prefix . 'rankforge_seo_queue';
    }

    public static function enqueue($post_id) {
        global $wpdb;
        $wpdb->insert(self::table_name(), [
            'post_id' => (int) $post_id,
            'status' => 'pending',
            'attempts' => 0,
            'last_error' => ''
        ]);
    }

    public static function next_batch($limit = 20) {
        global $wpdb;
        $limit = (int) $limit;
        return $wpdb->get_results("SELECT * FROM " . self::table_name() . " WHERE status = 'pending' ORDER BY id ASC LIMIT {$limit}");
    }
}
