<?php
// GENERATED CODE -- DO NOT EDIT!

namespace Grpc\Ouroboros;

/**
 * Ouroboros communication service definition.
 */
class OuroborosClient extends \Grpc\BaseStub {

    /**
     * @param string $hostname hostname
     * @param array $opts channel options
     * @param \Grpc\Channel $channel (optional) re-use channel object
     */
    public function __construct($hostname, $opts, $channel = null) {
        parent::__construct($hostname, $opts, $channel);
    }

    /**
     * A simple RPC.
     *
     * Obtains the `Response` based on the job asked in the `Request`
     * @param \Grpc\Ouroboros\Request $argument input argument
     * @param array $metadata metadata
     * @param array $options call options
     */
    public function SyncJob(\Grpc\Ouroboros\Request $argument,
      $metadata = [], $options = []) {
        return $this->_simpleRequest('/Grpc.Ouroboros.Ouroboros/SyncJob',
        $argument,
        ['\Grpc\Ouroboros\Response', 'decode'],
        $metadata, $options);
    }

    /**
     * We have a method called `StreamJob` which takes
     * parameter called `Request` and returns the message `Response`
     *
     * The stream keyword is specified before both the request type and response
     * type to make it as bidirectional streaming RPC method.
     * @param array $metadata metadata
     * @param array $options call options
     */
    public function StreamJob($metadata = [], $options = []) {
        return $this->_bidiRequest('/Grpc.Ouroboros.Ouroboros/StreamJob',
        ['\Grpc\Ouroboros\Response','decode'],
        $metadata, $options);
    }

}
