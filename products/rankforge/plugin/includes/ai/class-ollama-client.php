<?php
namespace RankForge\AI;

class OllamaClient {
    public function generate($prompt) {
        $endpoint = 'http://192.168.10.80:11434/api/generate';

        $response = wp_remote_post($endpoint, [
            'headers' => ['Content-Type' => 'application/json'],
            'body' => json_encode([
                'model' => 'hermes3:8b',
                'prompt' => $prompt,
                'stream' => false
            ])
        ]);

        return json_decode(wp_remote_retrieve_body($response), true);
    }
}
