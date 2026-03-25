<?php
if (!defined('ABSPATH')) exit;

global $wpdb;

$seo_table = $wpdb->prefix . 'rankforge_seo_queue';
$image_table = $wpdb->prefix . 'rankforge_image_queue';

use RankForge\Queue\RetryHelper;

$seo_errors = RetryHelper::recent_errors($seo_table);
$image_errors = RetryHelper::recent_errors($image_table);
?>

<div class="wrap">
    <h1>RankForge Errors</h1>

    <h2>SEO Errors</h2>
    <table class="widefat">
        <thead><tr><th>Post ID</th><th>Error</th><th>Attempts</th></tr></thead>
        <tbody>
        <?php foreach ($seo_errors as $row): ?>
            <tr>
                <td><?php echo $row->post_id; ?></td>
                <td><?php echo esc_html($row->last_error); ?></td>
                <td><?php echo $row->attempts; ?></td>
            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>

    <h2>Image Errors</h2>
    <table class="widefat">
        <thead><tr><th>Post ID</th><th>Error</th><th>Attempts</th></tr></thead>
        <tbody>
        <?php foreach ($image_errors as $row): ?>
            <tr>
                <td><?php echo $row->post_id; ?></td>
                <td><?php echo esc_html($row->last_error); ?></td>
                <td><?php echo $row->attempts; ?></td>
            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>

    <form method="post">
        <?php submit_button('Retry SEO Errors', 'primary', 'retry_seo'); ?>
        <?php submit_button('Retry Image Errors', 'secondary', 'retry_images'); ?>
    </form>
</div>
