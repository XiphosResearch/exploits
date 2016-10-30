<?php

    /**
     * SabreAMF_Const 
     *
     * SabreAMF global constants
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    final class SabreAMF_Const {

        /**
         * AC_Flash
         *
         * Specifies FlashPlayer 6.0 - 8.0 client
         */
        const AC_Flash    = 0;

        /**
         * AC_FlashCom
         *
         * Specifies FlashCom / Flash Media Server client
         */
        const AC_FlashCom = 1;

        /**
         * AC_Flex
         *
         * Specifies a FlashPlayer 9.0 client
         */
        const AC_Flash9 = 3;

        /**
         * R_RESULT
         *
         * Normal result to a methodcall
         */
        const R_RESULT = 1;

        /**
         * R_STATUS
         *
         * Faulty result
         */
        const R_STATUS = 2;

        /**
         * R_DEBUG
         *
         * Result to a debug-header
         */
        const R_DEBUG  = 3;

        /**
         * AMF0 Encoding
         */
        const AMF0 = 0;

        /**
         * AMF3 Encoding
         */
        const AMF3 = 3;

        /**
         * AMF3 Encoding + flex messaging wrappers
         */
        const FLEXMSG = 16;

        /**
         * AMF HTTP Mimetype
         */
        const MIMETYPE = 'application/x-amf';

   }




    /**
     * SabreAMF_Message 
     * 
     * The Message class encapsulates either an entire request package or an entire result package; including an AMF enveloppe
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause)
     * @uses SabreAMF_AMF0_Serializer
     * @uses SabreAMF_AMF0_Deserializer
     */
    class SabreAMF_Message {

        /**
         * clientType
         *
         * @var int
         */
        private $clientType=0;
        /**
         * bodies 
         * 
         * @var array
         */
        private $bodies=array();
        /**
         * headers 
         * 
         * @var array
         */
        private $headers=array();

        /**
         * encoding 
         * 
         * @var int 
         */
        private $encoding = SabreAMF_Const::AMF0;

        /**
         * serialize 
         * 
         * This method serializes a request. It requires an SabreAMF_OutputStream as an argument to read
         * the AMF Data from. After serialization the Outputstream will contain the encoded AMF data.
         * 
         * @param SabreAMF_OutputStream $stream 
         * @return void
         */
        public function serialize(SabreAMF_OutputStream $stream) {

            $this->outputStream = $stream;
            $stream->writeByte(0x00);
            $stream->writeByte($this->encoding);
            $stream->writeInt(count($this->headers));
            
            foreach($this->headers as $header) {

                $serializer = new SabreAMF_AMF0_Serializer($stream);
                $serializer->writeString($header['name']);
                $stream->writeByte($header['required']==true);
                $stream->writeLong(-1);
                $serializer->writeAMFData($header['data']);
            }

            $stream->writeInt(count($this->bodies));


            foreach($this->bodies as $body) {
                $serializer = new SabreAMF_AMF0_Serializer($stream);
                $serializer->writeString($body['target']);
                $serializer->writeString($body['response']);
                $stream->writeLong(-1);
                
                switch($this->encoding) {

                    case SabreAMF_Const::AMF0 :
                        $serializer->writeAMFData($body['data']);
                        break;
                    case SabreAMF_Const::AMF3 :
                        $serializer->writeAMFData(new SabreAMF_AMF3_Wrapper($body['data']));
                        break;

                }

            }

        }

        /**
         * deserialize 
         * 
         * This method deserializes a request. It requires an SabreAMF_InputStream with valid AMF data. After
         * deserialization the contents of the request can be found through the getBodies and getHeaders methods
         *
         * @param SabreAMF_InputStream $stream 
         * @return void
         */
        public function deserialize(SabreAMF_InputStream $stream) {

            $this->headers = array();
            $this->bodies = array();

            $this->InputStream = $stream;

            $stream->readByte();
          
            $this->clientType = $stream->readByte();

            $deserializer = new SabreAMF_AMF0_Deserializer($stream);

            $totalHeaders = $stream->readInt();

            for($i=0;$i<$totalHeaders;$i++) {

                $header = array(
                    'name'     => $deserializer->readString(),
                    'required' => $stream->readByte()==true
                );
                $stream->readLong();
                $header['data']  = $deserializer->readAMFData(null,true);
                $this->headers[] = $header;    

            }
 
            $totalBodies = $stream->readInt();

            for($i=0;$i<$totalBodies;$i++) {

                try {
                    $target = $deserializer->readString();
                } catch (Exception $e) {
                    // Could not fetch next body.. this happens with some versions of AMFPHP where the body
                    // count isn't properly set. If this happens we simply stop decoding
                    break;
                }

                $body = array(
                    'target'   => $target,
                    'response' => $deserializer->readString(),
                    'length'   => $stream->readLong(),
                    'data'     => $deserializer->readAMFData(null,true)
                );
         
                if (is_object($body['data']) && $body['data'] instanceof SabreAMF_AMF3_Wrapper) {
                     $body['data'] = $body['data']->getData();
                     $this->encoding = SabreAMF_Const::AMF3;
                } else if (is_array($body['data']) && isset($body['data'][0]) && is_object($body['data'][0]) && $body['data'][0] instanceof SabreAMF_AMF3_Wrapper) {

                     if ( defined('SABREAMF_AMF3_PRESERVE_ARGUMENTS') ) {
                        $body['data'][0] = $body['data'][0]->getData();
                     } else {
                        $body['data'] = $body['data'][0]->getData();

                     }
                     
                     $this->encoding = SabreAMF_Const::AMF3;
                }

                $this->bodies[] = $body;    

            }


        }

        /**
         * getClientType 
         * 
         * Returns the ClientType for the request. Check SabreAMF_Const for possible (known) values
         * 
         * @return int 
         */
        public function getClientType() {

            return $this->clientType;

        }

        /**
         * getBodies 
         * 
         * Returns the bodies int the message
         * 
         * @return array 
         */
        public function getBodies() {

            return $this->bodies;

        }

        /**
         * getHeaders 
         * 
         * Returns the headers in the message
         * 
         * @return array 
         */
        public function getHeaders() {

            return $this->headers;

        }

        /**
         * addBody 
         *
         * Adds a body to the message
         * 
         * @param mixed $body 
         * @return void 
         */
        public function addBody($body) {

            $this->bodies[] = $body;

        }

        /**
         * addHeader 
         * 
         * Adds a message header
         * 
         * @param mixed $header 
         * @return void
         */
        public function addHeader($header) {

            $this->headers[] = $header;

        }

        /**
         * setEncoding 
         * 
         * @param int $encoding 
         * @return void
         */
        public function setEncoding($encoding) {

            $this->encoding = $encoding;

        }

        /**
         * getEncoding 
         * 
         * @return int 
         */
        public function getEncoding() {

            return $this->encoding; 

        }

    }



    /**
     * SabreAMF_OutputStream 
     *
     * This class provides methods to encode bytes, longs, strings, int's etc. to a binary format
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    class SabreAMF_OutputStream {

        /**
         * rawData 
         * 
         * @var string
         */
        private $rawData = '';

        /**
         * writeBuffer 
         * 
         * @param string $str 
         * @return void
         */
        public function writeBuffer($str) {
            $this->rawData.=$str;
        }

        /**
         * writeByte 
         * 
         * @param int $byte 
         * @return void
         */
        public function writeByte($byte) {

            $this->rawData.=pack('c',$byte);

        }

        /**
         * writeInt 
         * 
         * @param int $int 
         * @return void
         */
        public function writeInt($int) {

            $this->rawData.=pack('n',$int);

        }
        
        /**
         * writeDouble 
         * 
         * @param float $double 
         * @return void
         */
        public function writeDouble($double) {

            $bin = pack("d",$double);
            $testEndian = unpack("C*",pack("S*",256));
            $bigEndian = !$testEndian[1]==1;
            if ($bigEndian) $bin = strrev($bin);
            $this->rawData.=$bin;

        }

        /**
         * writeLong 
         * 
         * @param int $long 
         * @return void
         */
        public function writeLong($long) {

            $this->rawData.=pack("N",$long);


        }

        /**
         * getRawData 
         * 
         * @return string 
         */
        public function getRawData() {

            return $this->rawData;

        }


    }




    /**
     * SabreAMF_Serializer 
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */

    /**
     * Abstract Serializer
     *
     * This is the abstract serializer class. This is used by the AMF0 and AMF3 serializers as a base class
     */
    abstract class SabreAMF_Serializer {

        /**
         * stream 
         * 
         * @var SabreAMF_OutputStream 
         */
        protected $stream;

        /**
         * __construct 
         * 
         * @param SabreAMF_OutputStream $stream 
         * @return void
         */
        public function __construct(SabreAMF_OutputStream $stream) {

            $this->stream = $stream;

        }

        /**
         * writeAMFData 
         * 
         * @param mixed $data 
         * @param int $forcetype 
         * @return mixed 
         */
        public abstract function writeAMFData($data,$forcetype=null); 

        /**
         * getStream
         *
         * @return SabreAMF_OutputStream
         */
        public function getStream() {

            return $this->stream;

        }

        /**
         * getRemoteClassName 
         * 
         * @param string $localClass 
         * @return mixed 
         */
        protected function getRemoteClassName($localClass) {

            return SabreAMF_ClassMapper::getRemoteClass($localClass);

        } 

       /**
         * Checks wether the provided array has string keys and if it's not sparse.
         *
         * @param array $arr
         * @return bool
         */
        protected function isPureArray(array $array ) {
            $i=0;
            foreach($array as $k=>$v) {
                if ( $k !== $i ) {
                   return false;
                }
                $i++;
            }

            return true;
        }

    }


    /**
     * SabreAMF_Deserializer 
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */


    /**
     * SabreAMF_Deserializer 
     * 
     * This is the abstract Deserializer. The AMF0 and AMF3 classes descent from this class
     */
    abstract class SabreAMF_Deserializer {

        /**
         * stream 
         * 
         * @var SabreAMF_InputStream
         */
        protected $stream;

        /**
         * __construct 
         *
         * @param SabreAMF_InputStream $stream 
         * @return void
         */
        public function __construct(SabreAMF_InputStream $stream) {

            $this->stream = $stream;

        }

        /**
         * readAMFData 
         * 
         * Starts reading an AMF block from the stream
         * 
         * @param mixed $settype 
         * @return mixed 
         */
        public abstract function readAMFData($settype = null); 


        /**
         * getLocalClassName 
         * 
         * @param string $remoteClass 
         * @return mixed 
         */
        protected function getLocalClassName($remoteClass) {

            return SabreAMF_ClassMapper::getLocalClass($remoteClass);

        } 

   }



    /**
     * SabreAMF_AMF0_Const 
     * 
     * @package SabreAMF 
     * @subpackage AMF0
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    final class SabreAMF_AMF0_Const {

        const DT_NUMBER      = 0x00;
        const DT_BOOL        = 0x01;
        const DT_STRING      = 0x02;
        const DT_OBJECT      = 0x03;
        const DT_MOVIECLIP   = 0x04;
        const DT_NULL        = 0x05;
        const DT_UNDEFINED   = 0x06;
        const DT_REFERENCE   = 0x07;
        const DT_MIXEDARRAY  = 0x08;
        const DT_OBJECTTERM  = 0x09;
        const DT_ARRAY       = 0x0a;
        const DT_DATE        = 0x0b;
        const DT_LONGSTRING  = 0x0c;
        const DT_UNSUPPORTED = 0x0e;
        const DT_XML         = 0x0f;
        const DT_TYPEDOBJECT = 0x10;
        const DT_AMF3        = 0x11;

   }




    /**
     * SabreAMF_AMF0_Serializer 
     * 
     * @package SabreAMF
     * @subpackage AMF0
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause)
     * @uses SabreAMF_Const
     * @uses SabreAMF_AMF0_Const
     * @uses SabreAMF_AMF3_Serializer
     * @uses SabreAMF_AMF3_Wrapper
     * @uses SabreAMF_ITypedObject
     */
    class SabreAMF_AMF0_Serializer extends SabreAMF_Serializer {

        /**
         * writeAMFData 
         * 
         * @param mixed $data 
         * @param int $forcetype 
         * @return mixed 
         */
        public function writeAMFData($data,$forcetype=null) {

           //If theres no type forced we'll try detecting it
           if (is_null($forcetype)) {
                $type=false;

                // NULL type
                if (!$type && is_null($data))    $type = SabreAMF_AMF0_Const::DT_NULL;

                // Boolean
                if (!$type && is_bool($data))    $type = SabreAMF_AMF0_Const::DT_BOOL;

                // Number
                if (!$type && (is_int($data) || is_float($data))) $type = SabreAMF_AMF0_Const::DT_NUMBER;

                // String (a long one)
                if (!$type && is_string($data) && strlen($data)>65536) $type = SabreAMF_AMF0_Const::DT_LONGSTRING;

                // Normal string
                if (!$type && is_string($data))  $type = SabreAMF_AMF0_Const::DT_STRING;

                // Checking if its an array
                if (!$type && is_array($data))   {
		    if ( $this->isPureArray( $data ) ) {
			$type = SabreAMF_AMF0_Const::DT_ARRAY;
		    } else {
		    	$type = SabreAMF_AMF0_Const::DT_MIXEDARRAY;
		    }
                }

                // Its an object
                if (!$type && is_object($data)) {

                    // If its an AMF3 wrapper.. we treat it as such
                    if ($data instanceof SabreAMF_AMF3_Wrapper) $type = SabreAMF_AMF0_Const::DT_AMF3;

                    else if ($data instanceof DateTime) $type = SabreAMF_AMF0_Const::DT_DATE;

                    // We'll see if its registered in the classmapper
                    else if ($this->getRemoteClassName(get_class($data))) $type = SabreAMF_AMF0_Const::DT_TYPEDOBJECT;

                    // Otherwise.. check if it its an TypedObject
                    else if ($data instanceof SabreAMF_ITypedObject) $type = SabreAMF_AMF0_Const::DT_TYPEDOBJECT;

                    // If everything else fails, its a general object
                    else $type = SabreAMF_AMF0_Const::DT_OBJECT;
                }

                // If everything failed, throw an exception
                if ($type===false) {
                    throw new Exception('Unhandled data-type: ' . gettype($data));
                    return null;
                }
           } else $type = $forcetype;

           $this->stream->writeByte($type);

           switch ($type) {

                case SabreAMF_AMF0_Const::DT_NUMBER      : return $this->stream->writeDouble($data);
                case SabreAMF_AMF0_Const::DT_BOOL        : return $this->stream->writeByte($data==true);
                case SabreAMF_AMF0_Const::DT_STRING      : return $this->writeString($data);
                case SabreAMF_AMF0_Const::DT_OBJECT      : return $this->writeObject($data);
                case SabreAMF_AMF0_Const::DT_NULL        : return true;
                case SabreAMF_AMF0_Const::DT_MIXEDARRAY  : return $this->writeMixedArray($data);
                case SabreAMF_AMF0_Const::DT_ARRAY       : return $this->writeArray($data);
                case SabreAMF_AMF0_Const::DT_DATE        : return $this->writeDate($data);
                case SabreAMF_AMF0_Const::DT_LONGSTRING  : return $this->writeLongString($data);
                case SabreAMF_AMF0_Const::DT_TYPEDOBJECT : return $this->writeTypedObject($data);
                case SabreAMF_AMF0_Const::DT_AMF3        : return $this->writeAMF3Data($data);
                default                   :  throw new Exception('Unsupported type: ' . gettype($data)); return false;
 
           }

        }

        /**
         * writeMixedArray 
         * 
         * @param array $data 
         * @return void
         */
        public function writeMixedArray($data) {

            $this->stream->writeLong(0);
            foreach($data as $key=>$value) {
                $this->writeString($key);
                $this->writeAMFData($value);
            }
            $this->writeString('');
            $this->stream->writeByte(SabreAMF_AMF0_Const::DT_OBJECTTERM);

        }

        /**
         * writeArray 
         * 
         * @param array $data 
         * @return void
         */
        public function writeArray($data) {

            if (!count($data)) {
                $this->stream->writeLong(0);
            } else {
                end($data);
                $last = key($data);
                $this->stream->writeLong($last+1);
                for($i=0;$i<=$last;$i++) {
                    if (isset($data[$i])) {
                        $this->writeAMFData($data[$i]);
                    } else {
                        $this->stream->writeByte(SabreAMF_AMF0_Const::DT_UNDEFINED);
                    }
                }
            }

        }

        /**
         * writeObject 
         * 
         * @param object $data 
         * @return void
         */
        public function writeObject($data) {

            foreach($data as $key=>$value) {
                $this->writeString($key);
                $this->writeAmfData($value);
            }
            $this->writeString('');
            $this->stream->writeByte(SabreAMF_AMF0_Const::DT_OBJECTTERM);
            return true;

        }

        /**
         * writeString 
         * 
         * @param string $string 
         * @return void
         */
        public function writeString($string) {

            $this->stream->writeInt(strlen($string));
            $this->stream->writeBuffer($string);

        }

        /**
         * writeLongString 
         * 
         * @param string $string 
         * @return void
         */
        public function writeLongString($string) {

            $this->stream->writeLong(strlen($string));
            $this->stream->writeBuffer($string);

        }
       /**
         * writeTypedObject 
         * 
         * @param object $data 
         * @return void
         */
        public function writeTypedObject($data) {

            if ($data instanceof SabreAMF_ITypedObject) {
                    $classname = $data->getAMFClassName();
                $data = $data->getAMFData();
            } else $classname = $this->getRemoteClassName(get_class($data));

            $this->writeString($classname);
            return $this->writeObject($data);

        }


        /**
         * writeAMF3Data 
         * 
         * @param mixed $data 
         * @return void 
         */
        public function writeAMF3Data(SabreAMF_AMF3_Wrapper $data) {

            $serializer = new SabreAMF_AMF3_Serializer($this->stream);
            return $serializer->writeAMFData($data->getData());

        }

        /**
         * Writes a date object 
         * 
         * @param DateTime $data 
         * @return void
         */
        public function writeDate(DateTime $data) {

            $this->stream->writeDouble($data->format('U')*1000);

            // empty timezone
            $this->stream->writeInt(0);
        }

    }


    /**
     * SabreAMF_AMF0_Deserializer 
     * 
     * @package SabreAMF
     * @subpackage AMF0
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     * @uses SabreAMF_Const
     * @uses SabreAMF_AMF0_Const
     * @uses SabreAMF_AMF3_Deserializer
     * @uses SabreAMF_AMF3_Wrapper
     * @uses SabreAMF_TypedObject
     */
    class SabreAMF_AMF0_Deserializer extends SabreAMF_Deserializer {

        /**
         * refList 
         * 
         * @var array 
         */
        private $refList = array();

        /**
         * amf3Deserializer 
         * 
         * @var SabreAMF_AMF3_Deserializer 
         */
        private $amf3Deserializer = null;

        /**
         * readAMFData 
         * 
         * @param int $settype 
         * @param bool $newscope
         * @return mixed 
         */
        public function readAMFData($settype = null,$newscope = false) {

           if ($newscope) $this->refList = array();

           if (is_null($settype)) {
                $settype = $this->stream->readByte();
           }

           switch ($settype) {

                case SabreAMF_AMF0_Const::DT_NUMBER      : return $this->stream->readDouble();
                case SabreAMF_AMF0_Const::DT_BOOL        : return $this->stream->readByte()==true;
                case SabreAMF_AMF0_Const::DT_STRING      : return $this->readString();
                case SabreAMF_AMF0_Const::DT_OBJECT      : return $this->readObject();
                case SabreAMF_AMF0_Const::DT_NULL        : return null; 
                case SabreAMF_AMF0_Const::DT_UNDEFINED   : return null;
                case SabreAMF_AMF0_Const::DT_REFERENCE   : return $this->readReference();
                case SabreAMF_AMF0_Const::DT_MIXEDARRAY  : return $this->readMixedArray();
                case SabreAMF_AMF0_Const::DT_ARRAY       : return $this->readArray();
                case SabreAMF_AMF0_Const::DT_DATE        : return $this->readDate();
                case SabreAMF_AMF0_Const::DT_LONGSTRING  : return $this->readLongString();
                case SabreAMF_AMF0_Const::DT_UNSUPPORTED : return null;
                case SabreAMF_AMF0_Const::DT_XML         : return $this->readLongString();
                case SabreAMF_AMF0_Const::DT_TYPEDOBJECT : return $this->readTypedObject();
                case SabreAMF_AMF0_Const::DT_AMF3        : return $this->readAMF3Data();
                default                   :  throw new Exception('Unsupported type: 0x' . strtoupper(str_pad(dechex($settype),2,0,STR_PAD_LEFT))); return false;
 
           }

        }

        /**
         * readObject 
         * 
         * @return object 
         */
        public function readObject() {

            $object = array();
            $this->refList[] =& $object;
            while (true) {
                $key = $this->readString();
                $vartype = $this->stream->readByte();
                if ($vartype==SabreAMF_AMF0_Const::DT_OBJECTTERM) break;
                $object[$key] = $this->readAmfData($vartype);
            }
            if (defined('SABREAMF_OBJECT_AS_ARRAY')) {
                $object = (object)$object;
            }
            return $object;    

        }

        /**
         * readReference 
         * 
         * @return object 
         */
        public function readReference() {
            
            $refId = $this->stream->readInt();
            if (isset($this->refList[$refId])) {
                return $this->refList[$refId];
            } else {
                throw new Exception('Invalid reference offset: ' . $refId);
                return false;
            }

        }


        /**
         * readArray 
         * 
         * @return array 
         */
        public function readArray() {

            $length = $this->stream->readLong();
            $arr = array();
            $this->refList[]&=$arr;
            while($length--) $arr[] = $this->readAMFData();
            return $arr;

        }

        /**
         * readMixedArray 
         * 
         * @return array 
         */
        public function readMixedArray() {

            $highestIndex = $this->stream->readLong();
            return $this->readObject();

        }

       /**
         * readString 
         * 
         * @return string 
         */
        public function readString() {

            $strLen = $this->stream->readInt();
            return $this->stream->readBuffer($strLen);

        }

        /**
         * readLongString 
         * 
         * @return string 
         */
        public function readLongString() {

            $strLen = $this->stream->readLong();
            return $this->stream->readBuffer($strLen);

        }

        /**
         *  
         * readDate 
         * 
         * @return int 
         */
        public function readDate() {

            // Unix timestamp in seconds. We strip the millisecond part
            $timestamp = floor($this->stream->readDouble() / 1000);

            // we are ignoring the timezone
            $timezoneOffset = $this->stream->readInt();
            //if ($timezoneOffset > 720) $timezoneOffset = ((65536 - $timezoneOffset));
            //$timezoneOffset=($timezoneOffset * 60) - date('Z');

            $dateTime = new DateTime('@' . $timestamp);
            
            return $dateTime;

        }

        /**
         * readTypedObject 
         * 
         * @return object
         */
        public function readTypedObject() {

            $classname = $this->readString();

            $isMapped = false;

            if ($localClassname = $this->getLocalClassName($classname)) {
                $rObject = new $localClassname();
                $isMapped = true;
            } else {
                $rObject = new SabreAMF_TypedObject($classname,null);
            }
            $this->refList[] =& $rObject;

            $props = array();
            while (true) {
                $key = $this->readString();
                $vartype = $this->stream->readByte();
                if ($vartype==SabreAMF_AMF0_Const::DT_OBJECTTERM) break;
                $props[$key] = $this->readAmfData($vartype);
            }

            if ($isMapped) {
                foreach($props as $k=>$v) 
                    $rObject->$k = $v;
            } else {
                $rObject->setAMFData($props);
            }

            return $rObject;

        }
        
        /**
         * readAMF3Data 
         * 
         * @return SabreAMF_AMF3_Wrapper 
         */
        public function readAMF3Data() {

            $amf3Deserializer = new SabreAMF_AMF3_Deserializer($this->stream);
            return new SabreAMF_AMF3_Wrapper($amf3Deserializer->readAMFData());

        }


   }


    /**
     * SabreAMF_AMF3_Const 
     * 
     * @package SabreAMF
     * @subpackage AMF3
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    final class SabreAMF_AMF3_Const {

    	const DT_UNDEFINED   = 0x00;
        const DT_NULL        = 0x01;
        const DT_BOOL_FALSE  = 0x02;
        const DT_BOOL_TRUE   = 0x03;
        const DT_INTEGER     = 0x04;
        const DT_NUMBER      = 0x05;
        const DT_STRING      = 0x06;
        const DT_XML         = 0x07;
        const DT_DATE        = 0x08;
        const DT_ARRAY       = 0x09;
        const DT_OBJECT      = 0x0A;
        const DT_XMLSTRING   = 0x0B;
        const DT_BYTEARRAY   = 0x0C;

        const ET_PROPLIST     = 0x00;
        const ET_EXTERNALIZED = 0x01;
        const ET_SERIAL       = 0x02;
   }




    /**
     * SabreAMF_AMF3_Serializer 
     * 
     * @package SabreAMF
     * @subpackage AMF3
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @author Karl von Randow http://xk72.com/
     * @author Develar
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause)
     * @uses SabreAMF_Const
     * @uses SabreAMF_AMF3_Const
     * @uses SabreAMF_ITypedObject
     */
    class SabreAMF_AMF3_Serializer extends SabreAMF_Serializer {

        /**
         * writeAMFData 
         * 
         * @param mixed $data 
         * @param int $forcetype 
         * @return mixed 
         */
        public function writeAMFData($data,$forcetype=null) {

           if (is_null($forcetype)) {
               // Autodetecting data type
               $type=false;
               if (!$type && is_null($data))    $type = SabreAMF_AMF3_Const::DT_NULL;
               if (!$type && is_bool($data))    {
                    $type = $data?SabreAMF_AMF3_Const::DT_BOOL_TRUE:SabreAMF_AMF3_Const::DT_BOOL_FALSE;
                }
                if (!$type && is_int($data)) {
                    // We essentially only got 29 bits for integers
                    if ($data > 0xFFFFFFF || $data < -268435456) {
                        $type = SabreAMF_AMF3_Const::DT_NUMBER;
                    } else {
                        $type = SabreAMF_AMF3_Const::DT_INTEGER;
                    }
                }
                if (!$type && is_float($data))   $type = SabreAMF_AMF3_Const::DT_NUMBER;
                if (!$type && is_int($data))     $type = SabreAMF_AMF3_Const::DT_INTEGER;
                if (!$type && is_string($data))  $type = SabreAMF_AMF3_Const::DT_STRING;
                if (!$type && is_array($data))   $type = SabreAMF_AMF3_Const::DT_ARRAY; 
                if (!$type && is_object($data)) {

                    if ($data instanceof SabreAMF_ByteArray) 
                        $type = SabreAMF_AMF3_Const::DT_BYTEARRAY;
                    elseif ($data instanceof DateTime) 
                        $type = SabreAMF_AMF3_Const::DT_DATE;
                    else 
                        $type = SabreAMF_AMF3_Const::DT_OBJECT;
                    

                }
                if ($type===false) {
                    throw new Exception('Unhandled data-type: ' . gettype($data));
                    return null;
                }
                if ($type == SabreAMF_AMF3_Const::DT_INTEGER && ($data > 268435455 || $data < -268435456)) {
                    $type = SabreAMF_AMF3_Const::DT_NUMBER;
                }
           } else $type = $forcetype;

           $this->stream->writeByte($type);

           switch ($type) {

                case SabreAMF_AMF3_Const::DT_NULL        : break;
                case SabreAMF_AMF3_Const::DT_BOOL_FALSE  : break;
                case SabreAMF_AMF3_Const::DT_BOOL_TRUE   : break;
                case SabreAMF_AMF3_Const::DT_INTEGER     : $this->writeInt($data); break;
                case SabreAMF_AMF3_Const::DT_NUMBER      : $this->stream->writeDouble($data); break;
                case SabreAMF_AMF3_Const::DT_STRING      : $this->writeString($data); break;
                case SabreAMF_AMF3_Const::DT_DATE        : $this->writeDate($data); break;
                case SabreAMF_AMF3_Const::DT_ARRAY       : $this->writeArray($data); break;
                case SabreAMF_AMF3_Const::DT_OBJECT      : $this->writeObject($data); break; 
                case SabreAMF_AMF3_Const::DT_BYTEARRAY   : $this->writeByteArray($data); break;
                default                   :  throw new Exception('Unsupported type: ' . gettype($data)); return null; 
 
           }

        }

        /**
         * writeObject 
         * 
         * @param mixed $data 
         * @return void
         */
        public function writeObject($data) {
           
            $encodingType = SabreAMF_AMF3_Const::ET_PROPLIST;
            if ($data instanceof SabreAMF_ITypedObject) {

                $classname = $data->getAMFClassName();
                $data = $data->getAMFData();

            } else if (!$classname = $this->getRemoteClassName(get_class($data))) {

                
                $classname = '';

            } else {

                if ($data instanceof SabreAMF_Externalized) {

                    $encodingType = SabreAMF_AMF3_Const::ET_EXTERNALIZED;

                }

            }


            $objectInfo = 0x03;
            $objectInfo |= $encodingType << 2;

            switch($encodingType) {

                case SabreAMF_AMF3_Const::ET_PROPLIST :

                    $propertyCount=0;
                    foreach($data as $k=>$v) {
                        $propertyCount++;
                    }

                    $objectInfo |= ($propertyCount << 4);


                    $this->writeInt($objectInfo);
                    $this->writeString($classname);
                    foreach($data as $k=>$v) {

                        $this->writeString($k);

                    }
                    foreach($data as $k=>$v) {

                        $this->writeAMFData($v);

                    }
                    break;

                case SabreAMF_AMF3_Const::ET_EXTERNALIZED :

                    $this->writeInt($objectInfo);
                    $this->writeString($classname);
                    $this->writeAMFData($data->writeExternal());
                    break;
            }

        }

        /**
         * writeInt 
         * 
         * @param int $int 
         * @return void
         */
        public function writeInt($int) {

    			// Note that this is simply a sanity check of the conversion algorithm;
    			// when live this sanity check should be disabled (overflow check handled in this.writeAMFData).
    			/*if ( ( ( $int & 0x70000000 ) != 0 ) && ( ( $int & 0x80000000 ) == 0 ) )
    				throw new Exception ( 'Integer overflow during Int32 to AMF3 conversion' );*/

    			if ( ( $int & 0xffffff80 ) == 0 )
    			{
    				$this->stream->writeByte ( $int & 0x7f );

    				return;
    			}

    			if ( ( $int & 0xffffc000 ) == 0 )
    			{
    				$this->stream->writeByte ( ( $int >> 7 ) | 0x80 );
    				$this->stream->writeByte ( $int & 0x7f );

    				return;
    			}

    			if ( ( $int & 0xffe00000 ) == 0 )
    			{
    				$this->stream->writeByte ( ( $int >> 14 ) | 0x80 );
    				$this->stream->writeByte ( ( $int >> 7 ) | 0x80 );
    				$this->stream->writeByte ( $int & 0x7f );

    				return;
    			}

    			$this->stream->writeByte ( ( $int >> 22 ) | 0x80 );
    			$this->stream->writeByte ( ( $int >> 15 ) | 0x80 );
    			$this->stream->writeByte ( ( $int >> 8 ) | 0x80 );
    			$this->stream->writeByte ( $int & 0xff );

    			return;
        }

        public function writeByteArray(SabreAMF_ByteArray $data) {

            $this->writeString($data->getData());

        }

        /**
         * writeString 
         * 
         * @param string $str 
         * @return void
         */
        public function writeString($str) {

            $strref = strlen($str) << 1 | 0x01;
            $this->writeInt($strref);
            $this->stream->writeBuffer($str);

        }

        /**
         * writeArray 
         * 
         * @param array $arr 
         * @return void
         */
        public function writeArray(array $arr) {

            //Check if this is an associative array or not.
            if ( $this->isPureArray( $arr ) ) {
              // Writing the length for the numeric keys in the array
              $arrLen = count($arr);
              $arrId = ($arrLen << 1) | 0x01;
  
              $this->writeInt($arrId);
              $this->writeString('');
  
              foreach($arr as $v) {
                  $this->writeAMFData($v);
              }

            } else {
                $this->writeInt(1);
                foreach($arr as $key=>$value) {
                    $this->writeString($key);
                    $this->writeAMFData($value);
                }
                $this->writeString('');

            }

        }
        
        /**
         * Writes a date object 
         * 
         * @param DateTime $data 
         * @return void
         */
        public function writeDate(DateTime $data) {

            // We're always sending actual date objects, never references
            $this->writeInt(0x01);
            $this->stream->writeDouble($data->format('U')*1000);

        }

    }


    /**
     * SabreAMF_AMF3_Deserializer 
     * 
     * @package SabreAMF
     * @subpackage AMF3
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @author Karl von Randow http://xk72.com/
     * @author Jim Mischel
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause)
     * @uses SabreAMF_Const
     * @uses SabreAMF_AMF3_Const
     * @uses SabreAMF_TypedObject
     */
    class SabreAMF_AMF3_Deserializer extends SabreAMF_Deserializer {

        /**
         * objectcount 
         * 
         * @var int
         */
        private $objectcount;

        /**
         * storedStrings 
         * 
         * @var array 
         */
        private $storedStrings = array();

        /**
         * storedObjects 
         * 
         * @var array 
         */
        private $storedObjects = array();

        /**
         * storedClasses 
         * 
         * @var array
         */
        private $storedClasses = array();

        /**
         * readAMFData 
         * 
         * @param mixed $settype 
         * @return mixed 
         */
        public function readAMFData($settype = null) {

           if (is_null($settype)) {
                $settype = $this->stream->readByte();
           }

           switch ($settype) {

                case SabreAMF_AMF3_Const::DT_UNDEFINED  : return null; 
                case SabreAMF_AMF3_Const::DT_NULL       : return null; 
                case SabreAMF_AMF3_Const::DT_BOOL_FALSE : return false;
                case SabreAMF_AMF3_Const::DT_BOOL_TRUE  : return true;
                case SabreAMF_AMF3_Const::DT_INTEGER    : return $this->readInt();
                case SabreAMF_AMF3_Const::DT_NUMBER     : return $this->stream->readDouble();
                case SabreAMF_AMF3_Const::DT_STRING     : return $this->readString();
                case SabreAMF_AMF3_Const::DT_XML        : return $this->readString();
                case SabreAMF_AMF3_Const::DT_DATE       : return $this->readDate();
                case SabreAMF_AMF3_Const::DT_ARRAY      : return $this->readArray();
                case SabreAMF_AMF3_Const::DT_OBJECT     : return $this->readObject();
                case SabreAMF_AMF3_Const::DT_XMLSTRING  : return $this->readXMLString();
                case SabreAMF_AMF3_Const::DT_BYTEARRAY  : return $this->readByteArray();
                default                   :  throw new Exception('Unsupported type: 0x' . strtoupper(str_pad(dechex($settype),2,0,STR_PAD_LEFT))); return false;


           }

        }


        /**
         * readObject 
         * 
         * @return object 
         */
        public function readObject() {

            $objInfo = $this->readU29();
            $storedObject = ($objInfo & 0x01)==0;
            $objInfo = $objInfo >> 1;

            if ($storedObject) {

                $objectReference = $objInfo;
                if (!isset($this->storedObjects[$objectReference])) {

                    throw new Exception('Object reference #' . $objectReference . ' not found');

                } else {

                    $rObject = $this->storedObjects[$objectReference];

                }

            } else {

                $storedClass = ($objInfo & 0x01)==0;
                $objInfo= $objInfo >> 1;

                // If this is a stored  class.. we have the info
                if ($storedClass) {
                  
                    $classReference = $objInfo;
                    if (!isset($this->storedClasses[$classReference])) {

                        throw new Exception('Class reference #' . $classReference . ' not found');

                    } else {

                        $encodingType = $this->storedClasses[$classReference]['encodingType'];
                        $propertyNames = $this->storedClasses[$classReference]['propertyNames'];
                        $className = $this->storedClasses[$classReference]['className'];

                    }
                  
                } else { 

                    $className = $this->readString();
                    $encodingType = $objInfo & 0x03;
                    $propertyNames = array();
                    $objInfo = $objInfo >> 2;

                }
                  
                //ClassMapping magic
                if ($className) {

                    if ($localClassName = $this->getLocalClassName($className)) {

                        $rObject = new $localClassName();

                    } else {

                        $rObject = new SabreAMF_TypedObject($className,array());

                    }
                } else {

                    $rObject = new STDClass(); 

                }

                $this->storedObjects[] =& $rObject;

                if ($encodingType & SabreAMF_AMF3_Const::ET_EXTERNALIZED) {

                    if (!$storedClass) {
                        $this->storedClasses[] = array('className' => $className,'encodingType'=>$encodingType,'propertyNames'=>$propertyNames);
                    }
                    if ($rObject instanceof SabreAMF_Externalized) {
                        $rObject->readExternal($this->readAMFData());
                    } elseif ($rObject instanceof SabreAMF_TypedObject) {
                        $rObject->setAMFData(array('externalizedData'=>$this->readAMFData()));
                    } else {
                        $rObject->externalizedData = $this->readAMFData();
                    }
                    //$properties['externalizedData'] = $this->readAMFData();

                } else {

                    if ($encodingType & SabreAMF_AMF3_Const::ET_SERIAL) {

                        if (!$storedClass) {
                            $this->storedClasses[] = array('className' => $className,'encodingType'=>$encodingType,'propertyNames'=>$propertyNames);
                        }
                        $properties = array();
                        do {
                            $propertyName = $this->readString();
                            if ($propertyName!="") {
                                $propertyNames[] = $propertyName;
                                $properties[$propertyName] = $this->readAMFData();
                            }
                        } while ($propertyName!="");
                        
                        
                    } else {
                        if (!$storedClass) {
                            $propertyCount = $objInfo;
                            for($i=0;$i<$propertyCount;$i++) {

                                $propertyNames[] = $this->readString();

                            }
                            $this->storedClasses[] = array('className' => $className,'encodingType'=>$encodingType,'propertyNames'=>$propertyNames);

                        }

                        $properties = array();
                        foreach($propertyNames as $propertyName) {

                            $properties[$propertyName] = $this->readAMFData();

                        }

                    }
                    
                    if ($rObject instanceof SabreAMF_TypedObject) {
                        $rObject->setAMFData($properties);
                    } else {
                        foreach($properties as $k=>$v) if ($k) $rObject->$k = $v;
                    }

                }

            }
            return $rObject;

        }

        /**
         * readArray 
         * 
         * @return array 
         */
        public function readArray() {

            $arrId = $this->readU29();
            if (($arrId & 0x01)==0) {
                 $arrId = $arrId >> 1;
                 if ($arrId>=count($this->storedObjects)) {
                    throw new Exception('Undefined array reference: ' . $arrId);
                    return false;
                }
                return $this->storedObjects[$arrId]; 
            }
            $arrId = $arrId >> 1;
            
            $data = array();
            $this->storedObjects[] &= $data;

            $key = $this->readString();

            while($key!="") {
                $data[$key] = $this->readAMFData();
                $key = $this->readString();
            }

            for($i=0;$i<$arrId;$i++) {
                $data[] = $this->readAMFData();
            }

            return $data;

        }
        

        /**
         * readString 
         * 
         * @return string 
         */
        public function readString() {

            $strref = $this->readU29();

            if (($strref & 0x01) == 0) {
                $strref = $strref >> 1;
                if ($strref>=count($this->storedStrings)) {
                    throw new Exception('Undefined string reference: ' . $strref);
                    return false;
                }
                return $this->storedStrings[$strref];
            } else {
                $strlen = $strref >> 1; 
                $str = $this->stream->readBuffer($strlen);
                if ($str != "") $this->storedStrings[] = $str;
                return $str;
            }

        }
        

        /**
         * readString 
         * 
         * @return string 
         */
        public function readXMLString() {

            $strref = $this->readU29();

            $strlen = $strref >> 1; 
            $str = $this->stream->readBuffer($strlen);
            return simplexml_load_string($str);

        }

        /**
         * readString 
         * 
         * @return string 
         */
        public function readByteArray() {

            $strref = $this->readU29();

            $strlen = $strref >> 1; 
            $str = $this->stream->readBuffer($strlen);
            return new SabreAMF_ByteArray($str);

        }

        /**
         * readU29 
         * 
         * @return int
         */
        public function readU29() {

            $count = 1;
            $u29 = 0;

            $byte = $this->stream->readByte();
  
            while((($byte & 0x80) != 0) && $count < 4) {
                $u29 <<= 7;
                $u29 |= ($byte & 0x7f);
                $byte = $this->stream->readByte();
                $count++;
            }
            
            if ($count < 4) {
                $u29 <<= 7;
                $u29 |= $byte;
            } else {
                // Use all 8 bits from the 4th byte
                $u29 <<= 8;
                $u29 |= $byte;
            }
            
            return $u29;
         
        }

        /**
         * readInt
         *
         * @return int
         */
        public function readInt() {
            
            $int = $this->readU29();
            // if int and has the sign bit set
            // Check if the integer is an int
            // and is signed
            if (($int & 0x18000000) == 0x18000000) {
                $int ^= 0x1fffffff;
                $int *= -1;
                $int -= 1;
            } else if (($int & 0x10000000) == 0x10000000) {
                // remove the signed flag
                $int &= 0x0fffffff;
            }

            return $int;

        }

        /**
         * readDate 
         * 
         * @return int 
         */
        public function readDate() {
            $dateref = $this->readU29();
            if (($dateref & 0x01) == 0) {
                $dateref = $dateref >> 1;
                if ($dateref>=count($this->storedObjects)) {
                    throw new Exception('Undefined date reference: ' . $dateref);
                    return false;
                }
                return $this->storedObjects[$dateref];
            }

            $timestamp = floor($this->stream->readDouble() / 1000);

            $dateTime = new DateTime('@' . $timestamp);
            
            $this->storedObjects[] = $dateTime;
            return $dateTime;
        }
 

    }




    /**
     * SabreAMF_AMF3_Wrapper 
     * 
     * @package SabreAMF
     * @subpackage AMF3
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    class SabreAMF_AMF3_Wrapper {


        /**
         * data 
         * 
         * @var mixed
         */
        private $data;


        /**
         * __construct 
         * 
         * @param mixed $data 
         * @return void
         */
        public function __construct($data) {

            $this->setData($data);

        }
        

        /**
         * getData 
         * 
         * @return mixed 
         */
        public function getData() {

            return $this->data;

        }

        /**
         * setData 
         * 
         * @param mixed $data 
         * @return void
         */
        public function setData($data) {

            $this->data = $data;

        }
            

    }




    /**
     * AMF Client
     *
     * Use this class to make a calls to AMF0/AMF3 services. The class makes use of the curl http library, so make sure you have this installed.
     *
     * It sends AMF0 encoded data by default. Change the encoding to AMF3 with setEncoding. sendRequest calls the actual service 
     * 
     * @package SabreAMF
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl/) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License
     * @example ../examples/client.php
     * @uses SabreAMF_Message
     * @uses SabreAMF_OutputStream
     * @uses SabreAMF_InputStream
     */
    class SabreAMF_Client {

        /**
         * endPoint 
         * 
         * @var string 
         */
        private $endPoint;
        /**
         * httpProxy
         * 
         * @var mixed
         */
        private $httpProxy;
        /**
         * amfInputStream 
         * 
         * @var SabreAMF_InputStream
         */
        private $amfInputStream;
        /**
         * amfOutputStream 
         * 
         * @var SabreAMF_OutputStream
         */
        private $amfOutputStream;

        /**
         * amfRequest 
         * 
         * @var SabreAMF_Message 
         */
        private $amfRequest;

        /**
         * amfResponse 
         * 
         * @var SabreAMF_Message 
         */
        private $amfResponse;

        /**
         * encoding 
         * 
         * @var int 
         */
        private $encoding = SabreAMF_Const::AMF0;

        /**
         * HTTP headers
         *
         * @var array
         */
        private $httpHeaders = array();

        /**
         * __construct 
         * 
         * @param string $endPoint The url to the AMF gateway
         * @return void
         */
        public function __construct($endPoint) {

            $this->endPoint = $endPoint;

            $this->amfRequest = new SabreAMF_Message();
            $this->amfOutputStream = new SabreAMF_OutputStream();

        }

        /**
         * Add a HTTP header to the cURL request
         *
         * @param string $header
         * @return $this
         */
        public function addHTTPHeader($header)
        {
            $this->httpHeaders[] = $header;

            return $this;
        }


        /**
         * sendRequest 
         *
         * sendRequest sends the request to the server. It expects the servicepath and methodname, and the parameters of the methodcall
         * 
         * @param string $servicePath The servicepath (e.g.: myservice.mymethod)
         * @param array $data The parameters you want to send
         * @return mixed 
         */
        public function sendRequest($servicePath,$data) {
           
            // We're using the FLEX Messaging framework
            if($this->encoding & SabreAMF_Const::FLEXMSG) {


                // Setting up the message
                $message = new SabreAMF_AMF3_RemotingMessage();
                $message->body = $data;

                // We need to split serviceName.methodName into separate variables
                $service = explode('.',$servicePath);
                $method = array_pop($service);
                $service = implode('.',$service);
                $message->operation = $method; 
                $message->source = $service;

                $data = $message;
            }

            $this->amfRequest->addBody(array(

                // If we're using the flex messaging framework, target is specified as the string 'null'
                'target'   => $this->encoding & SabreAMF_Const::FLEXMSG?'null':$servicePath,
                'response' => '/1',
                'data'     => $data
            ));

            $this->amfRequest->serialize($this->amfOutputStream);

            $headers = array_merge(array(
                'Content-type: ' . SabreAMF_Const::MIMETYPE
            ), $this->httpHeaders);

            // The curl request
            $ch = curl_init($this->endPoint);
            curl_setopt($ch,CURLOPT_POST,1);
            curl_setopt($ch,CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch,CURLOPT_TIMEOUT,20);
            curl_setopt($ch,CURLOPT_HTTPHEADER,$headers);
            curl_setopt($ch, CURLOPT_SSL_CIPHER_LIST, "ALL");
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            curl_setopt($ch, CURLOPT_COOKIEJAR, 'cookie.txt');
            curl_setopt($ch, CURLOPT_COOKIEFILE, 'cookie.txt');
            curl_setopt($ch,CURLOPT_POSTFIELDS,$this->amfOutputStream->getRawData());
    		if ($this->httpProxy) {
    			curl_setopt($ch,CURLOPT_PROXY,$this->httpProxy);
    		}
            $result = curl_exec($ch);
 
            if (curl_errno($ch)) {
                throw new Exception('CURL error: ' . curl_error($ch));
                false;
            } else {
                curl_close($ch);
            }
       
            $this->amfInputStream = new SabreAMF_InputStream($result);
            $this->amfResponse = new SabreAMF_Message(); 
            $this->amfResponse->deserialize($this->amfInputStream);

            $this->parseHeaders();

            foreach($this->amfResponse->getBodies() as $body) {

                if (strpos($body['target'],'/1')===0) return $body['data'] ;

            }

        }

        /**
         * addHeader 
         *
         * Add a header to the client request
         * 
         * @param string $name 
         * @param bool $required 
         * @param mixed $data 
         * @return void
         */
        public function addHeader($name,$required,$data) {

            $this->amfRequest->addHeader(array('name'=>$name,'required'=>$required==true,'data'=>$data));

        }
       
        /**
         * setCredentials 
         * 
         * @param string $username 
         * @param string $password 
         * @return void
         */
        public function setCredentials($username,$password) {

            $this->addHeader('Credentials',false,(object)array('userid'=>$username,'password'=>$password));

        }
        
        /**
         * setHttpProxy
         * 
         * @param mixed $httpProxy
         * @return void
         */
        public function setHttpProxy($httpProxy) {
            $this->httpProxy = $httpProxy;
        }

        /**
         * parseHeaders 
         * 
         * @return void
         */
        private function parseHeaders() {

            foreach($this->amfResponse->getHeaders() as $header) {

                switch($header['name']) {

                    case 'ReplaceGatewayUrl' :
                        if (is_string($header['data'])) {
                            $this->endPoint = $header['data'];
                        }
                        break;

                }


            }

        }

        /**
         * Change the AMF encoding (0 or 3) 
         * 
         * @param int $encoding 
         * @return void
         */
        public function setEncoding($encoding) {

            $this->encoding = $encoding;
            $this->amfRequest->setEncoding($encoding & SabreAMF_Const::AMF3);

        }

    }





    /**
     * SabreAMF_InputStream 
     * 
     * This is the InputStream class. You construct it with binary data and it can read doubles, longs, ints, bytes, etc. while maintaining the cursor position
     * 
     * @package SabreAMF 
     * @version $Id$
     * @copyright Copyright (C) 2006-2009 Rooftop Solutions. All rights reserved.
     * @author Evert Pot (http://www.rooftopsolutions.nl) 
     * @licence http://www.freebsd.org/copyright/license.html  BSD License (4 Clause) 
     */
    class SabreAMF_InputStream {

        /**
         * cursor 
         * 
         * @var int 
         */
        private $cursor = 0;
        /**
         * rawData 
         * 
         * @var string
         */
        private $rawData = '';


        /**
         * __construct 
         * 
         * @param string $data 
         * @return void
         */
        public function __construct($data) {

            //Rawdata has to be a string
            if (!is_string($data)) {
                throw new Exception('Inputdata is not of type String');
                return false;
            }
            $this->rawData = $data;

        }

        /**
         * &readBuffer 
         * 
         * @param int $length 
         * @return mixed 
         */
        public function &readBuffer($length) {

            if ($length+$this->cursor > strlen($this->rawData)) {
                throw new Exception('Buffer underrun at position: '. $this->cursor . '. Trying to fetch '. $length . ' bytes');
                return false;
            }
            $data = substr($this->rawData,$this->cursor,$length);
            $this->cursor+=$length;
            return $data;

        }

        /**
         * readByte 
         * 
         * @return int 
         */
        public function readByte() {

            return ord($this->readBuffer(1));

        }

        /**
         * readInt 
         * 
         * @return int 
         */
        public function readInt() {

            $block = $this->readBuffer(2);
            $int = unpack("n",$block);
            return $int[1];

        }


        /**
         * readDouble 
         * 
         * @return float 
         */
        public function readDouble() {

            $double = $this->readBuffer(8);

            $testEndian = unpack("C*",pack("S*",256));
            $bigEndian = !$testEndian[1]==1;
                        
            if ($bigEndian) $double = strrev($double);
            $double = unpack("d",$double);
            return $double[1];
        }

        /**
         * readLong 
         * 
         * @return int 
         */
        public function readLong() {

            $block = $this->readBuffer(4);
            $long = unpack("N",$block);
            return $long[1];
        }

        /**
         * readInt24 
         * 
         * return int 
         */
        public function readInt24() {

            $block = chr(0) . $this->readBuffer(3);
            $long = unpack("N",$block);
            return $long[1];

        }

    }



