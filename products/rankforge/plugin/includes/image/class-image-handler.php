<?php
namespace RankForge\Image;

class ImageHandler {

    public static function save_base64_image($base64, $post_id, $filename) {
        $upload = wp_upload_dir();

        $data = base64_decode($base64);
        $file = $upload['path'] . '/' . $filename . '.png';

        file_put_contents($file, $data);

        $attachment = [
            'post_mime_type' => 'image/png',
            'post_title' => $filename,
            'post_status' => 'inherit'
        ];

        $attach_id = wp_insert_attachment($attachment, $file, $post_id);
        require_once ABSPATH . 'wp-admin/includes/image.php';
        $attach_data = wp_generate_attachment_metadata($attach_id, $file);
        wp_update_attachment_metadata($attach_id, $attach_data);

        set_post_thumbnail($post_id, $attach_id);

        return $attach_id;
    }
}
