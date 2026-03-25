<?php
namespace RankForge\Queue;

if (!defined('ABSPATH')) exit;

class BackoffPolicy {
    public static function classify_error($message) {
        $message = strtolower((string) $message);

        if (strpos($message, 'timeout') !== false || strpos($message, 'connection') !== false || strpos($message, 'temporarily') !== false) {
            return 'transient';
        }

        if (strpos($message, 'invalid json') !== false || strpos($message, 'bad request') !== false || strpos($message, 'prompt') !== false) {
            return 'content';
        }

        if (strpos($message, 'not found') !== false || strpos($message, 'missing model') !== false || strpos($message, '404') !== false) {
            return 'configuration';
        }

        return 'unknown';
    }

    public static function next_delay_seconds($attempts) {
        $attempts = max(1, (int) $attempts);
        $base = 60;
        $max = 3600;
        $delay = $base * pow(2, $attempts - 1);
        return min($max, (int) $delay);
    }

    public static function should_retry($message, $attempts, $max_attempts = 5) {
        $attempts = (int) $attempts;
        $max_attempts = (int) $max_attempts;
        $class = self::classify_error($message);

        if ($attempts >= $max_attempts) {
            return false;
        }

        if ($class === 'configuration' || $class === 'content') {
            return false;
        }

        return true;
    }
}
