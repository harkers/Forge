<?php
namespace RankForge\Queue;

use RankForge\AI\OllamaClient;
use RankForge\AI\SDClient;

class WorkerV2 {

    public static function process_seo($limit = 10) {
        if (!Lock::acquire('rankforge_seo_lock')) return;

        $items = SEOQueue::next_batch($limit);
        $ai = new OllamaClient();

        foreach ($items as $item) {
            $post_id = $item->post_id;

            try {
                $result = $ai->generate("Generate SEO title and meta description for: " . get_the_title($post_id));
                update_post_meta($post_id, '_rankforge_seo_raw', json_encode($result));
                SEOQueue::mark_complete($item->id);
            } catch (\Exception $e) {
                SEOQueue::mark_error($item->id, $e->getMessage());
            }
        }

        Lock::release('rankforge_seo_lock');
    }

    public static function process_images($limit = 10) {
        if (!Lock::acquire('rankforge_image_lock')) return;

        $items = ImageQueue::next_batch($limit);
        $sd = new SDClient();

        foreach ($items as $item) {
            $post_id = $item->post_id;

            try {
                $result = $sd->generate(get_the_title($post_id));
                update_post_meta($post_id, '_rankforge_image_raw', json_encode($result));
                ImageQueue::mark_complete($item->id);
            } catch (\Exception $e) {
                ImageQueue::mark_error($item->id, $e->getMessage());
            }
        }

        Lock::release('rankforge_image_lock');
    }
}
