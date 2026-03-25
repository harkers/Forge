<?php
namespace RankForge\Core;

use RankForge\Queue\WorkerV2;

if (!defined('ABSPATH')) exit;

class Cron {

    public static function init() {
        add_filter('cron_schedules', [__CLASS__, 'add_intervals']);

        add_action('rankforge_process_seo_queue', [__CLASS__, 'run_seo']);
        add_action('rankforge_process_image_queue', [__CLASS__, 'run_images']);

        if (!wp_next_scheduled('rankforge_process_seo_queue')) {
            wp_schedule_event(time(), 'rankforge_five_minutes', 'rankforge_process_seo_queue');
        }

        if (!wp_next_scheduled('rankforge_process_image_queue')) {
            wp_schedule_event(time(), 'rankforge_five_minutes', 'rankforge_process_image_queue');
        }
    }

    public static function add_intervals($schedules) {
        $schedules['rankforge_five_minutes'] = [
            'interval' => 300,
            'display' => 'Every 5 Minutes'
        ];
        return $schedules;
    }

    public static function run_seo() {
        WorkerV2::process_seo(10);
    }

    public static function run_images() {
        WorkerV2::process_images(5);
    }
}
