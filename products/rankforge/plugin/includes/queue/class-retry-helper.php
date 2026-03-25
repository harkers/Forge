<?php
namespace RankForge\Queue;

if (!defined('ABSPATH')) exit;

class RetryHelper {
    public static function retry_errors($table_name, $max_attempts = 3, $limit = 50) {
        global $wpdb;

        $max_attempts = (int) $max_attempts;
        $limit = (int) $limit;

        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT id FROM {$table_name} WHERE status = 'error' AND attempts < %d ORDER BY updated_at ASC LIMIT %d",
            $max_attempts,
            $limit
        ));

        foreach ($rows as $row) {
            $wpdb->update($table_name, [
                'status' => 'pending',
                'last_error' => ''
            ], [
                'id' => (int) $row->id
            ]);
        }

        return count($rows);
    }

    public static function recent_errors($table_name, $limit = 20) {
        global $wpdb;
        $limit = (int) $limit;
        return $wpdb->get_results("SELECT * FROM {$table_name} WHERE status = 'error' ORDER BY updated_at DESC LIMIT {$limit}");
    }
}
