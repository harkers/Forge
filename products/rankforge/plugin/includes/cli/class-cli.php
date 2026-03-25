<?php
namespace RankForge\CLI;

use RankForge\Queue\WorkerV2;
use RankForge\Queue\ImageQueue;

if (!defined('ABSPATH')) exit;

class CLI {
    public static function register() {
        if (!defined('WP_CLI') || !WP_CLI) {
            return;
        }

        \WP_CLI::add_command('rankforge process-seo-queue', [__CLASS__, 'process_seo_queue']);
        \WP_CLI::add_command('rankforge process-image-queue', [__CLASS__, 'process_image_queue']);
        \WP_CLI::add_command('rankforge enqueue-missing-images', [__CLASS__, 'enqueue_missing_images']);
    }

    public static function process_seo_queue($args, $assoc_args) {
        $limit = isset($assoc_args['limit']) ? (int) $assoc_args['limit'] : 10;
        WorkerV2::process_seo($limit);
        \WP_CLI::success('Processed SEO queue batch.');
    }

    public static function process_image_queue($args, $assoc_args) {
        $limit = isset($assoc_args['limit']) ? (int) $assoc_args['limit'] : 10;
        WorkerV2::process_images($limit);
        \WP_CLI::success('Processed image queue batch.');
    }

    public static function enqueue_missing_images($args, $assoc_args) {
        $post_types = isset($assoc_args['post_type']) ? [(string) $assoc_args['post_type']] : ['post'];

        $query = new \WP_Query([
            'post_type' => $post_types,
            'post_status' => 'publish',
            'posts_per_page' => -1,
            'fields' => 'ids',
            'meta_query' => [
                [
                    'key' => '_thumbnail_id',
                    'compare' => 'NOT EXISTS'
                ]
            ]
        ]);

        $count = 0;
        foreach ($query->posts as $post_id) {
            ImageQueue::enqueue($post_id);
            $count++;
        }

        \WP_CLI::success("Enqueued {$count} posts missing featured images.");
    }
}
