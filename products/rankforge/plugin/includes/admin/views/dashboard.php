<?php
if (!defined('ABSPATH')) exit;

global $wpdb;

$seo_table = $wpdb->prefix . 'rankforge_seo_queue';
$image_table = $wpdb->prefix . 'rankforge_image_queue';

$seo_counts = $wpdb->get_results("SELECT status, COUNT(*) as count FROM {$seo_table} GROUP BY status", OBJECT_K);
$image_counts = $wpdb->get_results("SELECT status, COUNT(*) as count FROM {$image_table} GROUP BY status", OBJECT_K);

function rf_count($arr, $key) {
    return isset($arr[$key]) ? $arr[$key]->count : 0;
}
?>

<div class="wrap">
    <h1>RankForge Dashboard</h1>

    <h2>SEO Queue</h2>
    <ul>
        <li>Pending: <?php echo rf_count($seo_counts, 'pending'); ?></li>
        <li>Processing: <?php echo rf_count($seo_counts, 'processing'); ?></li>
        <li>Complete: <?php echo rf_count($seo_counts, 'complete'); ?></li>
        <li>Error: <?php echo rf_count($seo_counts, 'error'); ?></li>
    </ul>

    <h2>Image Queue</h2>
    <ul>
        <li>Pending: <?php echo rf_count($image_counts, 'pending'); ?></li>
        <li>Processing: <?php echo rf_count($image_counts, 'processing'); ?></li>
        <li>Complete: <?php echo rf_count($image_counts, 'complete'); ?></li>
        <li>Error: <?php echo rf_count($image_counts, 'error'); ?></li>
    </ul>

    <hr>

    <form method="post">
        <?php submit_button('Process SEO Queue', 'primary', 'process_seo'); ?>
        <?php submit_button('Process Image Queue', 'secondary', 'process_images'); ?>
    </form>
</div>
