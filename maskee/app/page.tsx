"use client"
import React, { useEffect, useState } from 'react'
import {Sparkles,ScanFace,ShieldCheck,RotateCcw,LoaderCircle} from "lucide-react"
import Upload from '@/components/upload'
import { Placeholder,Success,Failure,Error } from '@/components/result'


type OutputType = {
        Success : boolean,
        Similarity? : number,
        "Adaptive Threshold"? : number,
        Match? : boolean,
        Message? : string
    }

function Home() {
  const [active , setActive]  = useState<boolean>(false);
  const [output,setOutput] = useState<OutputType | null>(null);
  const [loading,setLoading] = useState<boolean>(false);

  const [image1 ,setImage1] = useState<File|null>(null);
  const [image2 ,setImage2] = useState<File|null>(null);

  
  useEffect(()=>{
    if(image1 && image2) setActive(true);
    else setActive(false);
  },[image1,image2]);
  
  
  const url_endpoint = "http://localhost:5000/analyze";

  const handleSubmit = async(e:any)=>{
    e.preventDefault();
    if(!image1 || !image2) return;
    setLoading(true);
    try{
      const formData = new FormData();
      formData.append('image1', image1);
      formData.append('image2', image2);

      const result = await fetch(url_endpoint,{
        method:"Post",
        body:formData
      })

      const parsedResult = await result.json();
      if(!parsedResult) return console.error("Unable to process");

      setOutput(parsedResult);
  }catch(err){
    console.error(err);
  }finally{
    setLoading(false);
  }

  }


  const resetForm = ()=>{
    setActive(false);
    setOutput(null);
    setImage1(null);
    setImage2(null);
  }



  return (
    <div className='min-h-screen h-fit w-screen home_bg flex flex-col justify-center items-center gap-5 py-20' >
      <div className='flex gap-3 items-center border border-gray-600/50 text-gray-300/80 px-3 py-1 rounded-2xl text-sm bg-black/20'> <Sparkles size={16} className='text-purple-300/80'/> AI powered identity verification</div>
      <h1 className='text-6xl font-bold tracking-tighter bg-linear-to-r  from-violet-400  to-cyan-400 text-transparent bg-clip-text'>Match Masked & Unmasked Faces</h1>
      <p className='w-1/2 text-center text-xl text-gray-400'>Upload one masked photo and one unmasked photo. Our AI compares facial geometry to determine if they belong to the same person — in seconds.</p>
      <div className='w-15/20 h-fit flex justify-between mt-5'>
        <Upload title='Masked Image' sub_title='Face partially covered (mask, scarf, etc.)' Icon={ScanFace} id_upload='AG&-EJD' state={image1} changeStateMethod={setImage1}/>
        <Upload title='Unmasked Image' sub_title='Clear, fully visible face' Icon={ShieldCheck} id_upload='A#@-G^E' state={image2} changeStateMethod={setImage2}/>
      </div>
      <div className='w-fit h-fit mt-10 flex items-center gap-5'>
        <button className={
          active ? 'cursor-pointer flex items-center gap-2  text-black  w-40 justify-center py-3 px-4 text-sm rounded-md bg-linear-to-r from-violet-500 to-cyan-400':
          'cursor-pointer flex items-center gap-2  text-black  w-40 justify-center py-3 px-4 text-sm rounded-md bg-linear-to-r from-violet-500/40 to-cyan-400/40'
        }
        onClick={handleSubmit}
        >
          {loading ? <LoaderCircle className='animate-spin'/> : <>
          <ScanFace size={18}/> Verify Match
          </>}
          
          </button>


        <button className={
          active ? "cursor-pointer flex items-center gap-2 text-white w-40 justify-center py-3 px-4 text-sm rounded-md":
          'cursor-pointer flex items-center gap-2 text-white/50 w-40 justify-center py-3 px-4 text-sm rounded-md'
        }
        onClick={resetForm}
        ><RotateCcw size={18}/> Reset</button>
      </div>

      {
      output===null ? <Placeholder/> :
      (
        <>
          {output.Success ? 
            <>
            {output.Match ? <Success output={output}/> : <Failure output={output}/>}
            </> 
          : <Error output={output}/>}
        </>
      )
      
      }


      <p className='text-xs text-slate-400'>Images are processed securely. Nothing is stored after verification.</p>

    </div>
  )
}

export default Home