<?php
namespace RankForge\Queue;

class Lock {
    public static function acquire($key, $ttl = 300) {
        if (get_transient($key)) return false;
        set_transient($key, 1, $ttl);
        return true;
    }

    public static function release($key) {
        delete_transient($key);
    }
}
