import axios from "axios";
import React,{useEffect, useState} from "react";
import { useDispatch } from "react-redux/es/hooks/useDispatch";
import { useSelector } from "react-redux/es/hooks/useSelector";
import { detectLang, outputText } from "../redux/actions";

const Convert=({options})=>{
    const dispatch=useDispatch();
    const text=useSelector(state=>state.text.inputText);
    const [debouncedText, setDebouncedText]=useState(text);
    const inLang=useSelector(state=>state.language.inLang);
    const outLang=useSelector(state=>state.language.outLang);
    const output=useSelector(state=>state.text.outputText);
    useEffect(()=>{
        
        const timer=setTimeout(()=>{
            setDebouncedText(text);
        },300);
        
        return ()=>{clearTimeout(timer);};
    },[text,inLang,outLang]);


    useEffect(()=>{
        const doDetection=async()=>{
            const {data}=await axios.post('http://127.0.0.1:8081/detect',{
                    text:debouncedText,
            });
            if(inLang.value!==data.language && debouncedText!==""){
                document.getElementById("suggestion").style.display="block";
                options.forEach(option => {
                    if(option.value===data.language){
                        dispatch(detectLang(option));
                    }
                });
            }
            else{
                document.getElementById("suggestion").style.display="none";
            }
            
        };
        doDetection();
    },[debouncedText, inLang,options]);

    useEffect(()=>{
        
        const doTranslation=async()=>{
            /*const {data}=await fetch('http://127.0.0.1:5001/translate', {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' },
                mode:'cors',
                body:JSON.stringify( {
                    text:debouncedText,
                    target:outLang.value,
                    source:inLang.value,
                })
          
              })*/
            const {data}=await axios.post('http://127.0.0.1:8081/translate',{
                text:debouncedText,
                target:outLang.value,
                source:inLang.value,
            }/*,{
                params:{
                    text:debouncedText,
                    target:outLang.value,
                    source:inLang.value,
                }
            }*/);
            dispatch(outputText(data.translatedtext));
        };
        doTranslation();
    },[debouncedText, inLang,outLang]);

    if(output===""){
        return(<div className="m-4 text-muted"><h2>Translate</h2></div>);
    }
    return(<div className="m-4" style={{ color: "black"}}><h2>{output}</h2></div>); 

}


export default Convert;