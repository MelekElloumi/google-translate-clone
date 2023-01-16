import axios from "axios";
import React, { useEffect, useState } from "react";
import ReactPlayer from 'react-audio-player';

function TextToSpeech({ text, language }) {
    //const [text, setText] = useState('');
    const [audioUrl, setAudioUrl] = useState(null);

    async function handleSubmit() {
      // Call the REST API endpoint with the text
      /*const response = await fetch("http://127.0.0.1:5000/tts?text=${text}&language=${language}");
      const audioUrl = await response.text();*/
      console.log(text,language);
      axios.get(`http://127.0.0.1:8080/tts?text=${text}&language=${language}`, {responseType: 'arraybuffer'})
      .then(response => {
        const blob = new Blob([response.data], { type: 'audio/mp3' });
        setAudioUrl(URL.createObjectURL(blob));
      });
      // Update the state with the URL of the audio file
      //setAudioUrl(audioUrl);
    }
  
    return (
      <div>
        <button onClick={handleSubmit} style={{backgroundColor:"white",display: "inline-block",border: "none"}}><i className='fas fa-volume-up text-secondary'></i>
        </button>
        {audioUrl && (
           <ReactPlayer
           src={audioUrl}
           type="audio/mp3"
           autoPlay
            />
        )}
      </div>
    );
}

export default TextToSpeech;