<?php
namespace RankForge\Queue;

if (!defined('ABSPATH')) exit;

class DeadLetter {
    public static function move($table_name, $id, $reason) {
        global $wpdb;

        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table_name} WHERE id = %d", (int) $id), ARRAY_A);
        if (!$row) return;

        $dlq_table = $table_name . '_dlq';

        $wpdb->insert($dlq_table, [
            'original_id' => $row['id'],
            'post_id' => $row['post_id'],
            'status' => 'dead',
            'attempts' => $row['attempts'],
            'last_error' => $reason,
            'created_at' => current_time('mysql')
        ]);

        $wpdb->delete($table_name, ['id' => (int) $id]);
    }
}
