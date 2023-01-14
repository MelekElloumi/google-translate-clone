import React, { useEffect, useState } from "react";
import AudioPlayer from 'react-audio-player';

function TextToSpeech({ text },{ language }) {
    //const [text, setText] = useState('');
    const [audioUrl, setAudioUrl] = useState(null);
  
    async function handleSubmit() {
      // Call the REST API endpoint with the text
      const response = await fetch("/api/text-to-speech?text=${texts}");
      const audioUrl = await response.text();
  
      // Update the state with the URL of the audio file
      setAudioUrl(audioUrl);
    }
  
    return (
      <div>
        <button onClick={handleSubmit}><i className='fas fa-volume-up text-secondary'></i>
        </button>
        {audioUrl && (
          <AudioPlayer
            src={audioUrl}
            autoPlay
          />
        )}
      </div>
    );
}

export default TextToSpeech;