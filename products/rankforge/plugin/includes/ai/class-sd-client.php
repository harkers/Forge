<?php
namespace RankForge\AI;

class SDClient {
    public function generate($prompt) {
        $endpoint = 'http://localhost:7860/sdapi/v1/txt2img';

        $payload = [
            'prompt' => $prompt,
            'negative_prompt' => 'blurry, low quality, noise, watermark, text, logo, ugly, deformed',
            'steps' => 25,
            'width' => 1024,
            'height' => 512,
            'cfg_scale' => 7,
            'sampler_name' => 'DPM++ 2M Karras',
            'override_settings' => [
                'sd_model_checkpoint' => 'dreamshaperXL10.safetensors',
                'sd_vae' => 'Automatic'
            ]
        ];

        $response = wp_remote_post($endpoint, [
            'headers' => ['Content-Type' => 'application/json'],
            'body' => json_encode($payload)
        ]);

        return json_decode(wp_remote_retrieve_body($response), true);
    }
}
