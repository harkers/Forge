<?php
namespace RankForge\Queue;

class SEOQueueV2 {
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

    public static function mark_processing($id) {
        global $wpdb;
        $wpdb->update(self::table_name(), ['status' => 'processing'], ['id' => (int) $id]);
    }

    public static function mark_complete($id) {
        global $wpdb;
        $wpdb->update(self::table_name(), ['status' => 'complete'], ['id' => (int) $id]);
    }

    public static function mark_error($id, $error) {
        global $wpdb;
        $wpdb->query($wpdb->prepare(
            "UPDATE " . self::table_name() . " SET status = 'error', attempts = attempts + 1, last_error = %s WHERE id = %d",
            (string) $error,
            (int) $id
        ));
    }
}
