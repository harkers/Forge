<?php
namespace RankForge\Queue;

use RankForge\AI\OllamaClient;
use RankForge\AI\SDClient;

class Worker {

    public static function process_seo($limit = 10) {
        $items = SEOQueue::next_batch($limit);
        $ai = new OllamaClient();

        foreach ($items as $item) {
            $post_id = $item->post_id;
            $prompt = "Generate SEO title and meta description for post ID {$post_id}";

            $result = $ai->generate($prompt);

            update_post_meta($post_id, '_rankforge_seo_raw', json_encode($result));
        }
    }

    public static function process_images($limit = 10) {
        $items = ImageQueue::next_batch($limit);
        $sd = new SDClient();

        foreach ($items as $item) {
            $post_id = $item->post_id;
            $prompt = get_the_title($post_id);

            $image = $sd->generate($prompt);

            update_post_meta($post_id, '_rankforge_image_raw', json_encode($image));
        }
    }
}
