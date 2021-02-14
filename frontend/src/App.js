import logo from './logo.svg';
import moanaImg from './moana.jpg';
import rapunzelImg from './rapunzel.png';
import shrekImg from './shrek.jpg';
// import Teacher from './Teacher'
import './App.css';
import { Form, Button, FormGroup, FormControl, ControlLabel,InputGroup,Navbar,Nav,NavDropdown, DropdownButton,Dropdown } from "react-bootstrap";
// import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, {useState} from 'react'

function App() {
  // var result = {};
  const divStyle = {
    color: 'black',
    textAlign:'left',
    margin:'50px'
  };
  // state = { showing: true };
  const[loading,setLoading] =useState(false)
  const [name,setName]=useState("");
  const [rapunzel,setRapunzel]=useState(false);
  const [moana,setMoana]=useState(false);
  const [shrek,setShrek]=useState(false);
  const [summary,setSummary]=useState(false);
  const [topic,setTopic]=useState("");
  const [similar,setSimilar]=useState(false);
  const [quiz,setQuiz]=useState(false);
  const [simple,setSimple]=useState(false);
  const [dates,setDates]=useState([]);
  const [result,setResult] = useState(false)
  const [video,setVideo] = useState(false)
  const[sumText,setSumText] = useState("")
  const[ques,setQ] = useState([])
  const[ans,setA] = useState([])
  const[simpText,setSimpText] = useState("")
  const[sched,setsched] = useState([])
  const[link,setLink] = useState("")
  const[transcript,setTranscript] = useState("")
  const [showResults, setShowResults] = useState(false)
  // const [checked, setChecked] = useState(false)
  // const [status, setStatus] = useState(true)
  const onClick = () => setShowResults(true)


  const[chechbookname,setCheckbookName] = useState("")
  const[chechbookrecepient,setCheckbookRecepient] = useState("")
  const[chechbookamount,setCheckbookAmount] = useState("")
  const[chechbookdesc,setCheckbookDesc] = useState("")
  const[chechbookimg,setCheckbookImage] = useState("")
  const[ischeckbook,setischeck] = useState(false)

  const [arrayTopic, setarrayTopic] = useState(["Basketball", "Football", "Fortnite","History"])
  const Add = arrayTopic.map(Add => Add
  )
  const handleTopicTypeChange = (e) => setTopic(arrayTopic[e.target.value])

  // const onChangeHandler = () => {
  //   setChecked(!checked);
  //   setStatus(false);
  // };

  // const [interest,setInterest]=useState("");
  const submit = e => {
    // e.preventDefault()
    setLoading(true)
    fetch('http://10.0.0.10:5000/getAudioAnalysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"location":name,"rapunzel":rapunzel,"moana":moana, "shrek":shrek,"summarize":summary,"qna":quiz,"simplify":simple,"dates":dates, "similar":similar,"topic":topic})
        })
        .then(response => response.json())
        .then(
            data => {
                console.log(data)
                console.log({"location":name,"rapunzel":rapunzel,"moana":moana, "shrek":shrek,"summarize":summary,"qna":quiz,"simplify":simple,"dates":dates, "similar":similar,"topic":topic})
                setResult(true)
                setVideo(true)
                setsched(data.dates)
                setSimilar(data.similar)
                setSumText(data.summarize)
                setSimpText(data.simplify)
                setA(data.qna.answers)
                setQ(data.qna.questions)
                setLink(data.videoLink)
                setTranscript(data.transcript)
                setLoading(false)
            })
        .catch(error => console.error(error))
    // fetch('10.0.0.10:5000/getAudioAnalysis', {
    //   method: 'POST',
    //   body: JSON.stringify({"name":name,"mickey":0,"donald":1, "shrek":0,"summary":1,"quiz":1,"simple":0,"dates":0})
    // })
    
    //   .then(response => response.json())
    //   .then(data => {
    //     console.log('In')
    //     console.log(data)
    //   })
      
      // .then(json => setUser(json.user))

    // console.log(JSON.stringify({ "location":name,"mickey":mickey,"donald":donald,"shrek":shrek,"summarize":summary,"qna":quiz,"simplify":simple,"dates":dates }))
  }

  const checkbook = e => { fetch('http://10.0.0.10:5000/sendMoney', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({"name":chechbookname,"recipient":chechbookrecepient,"amount":chechbookamount, "description":chechbookdesc})
})
.then(response => response.json())
.then(
    data => {
      console.log({"name":chechbookname,"recipient":chechbookrecepient,"amount":chechbookamount, "description":chechbookdesc})
      console.log(data)
      setCheckbookImage(data.image_uri)
      setischeck(true)
    })
  }

  // const appStyle = {
  //   backgroundColor: "black"
  // };

  return (
    <div className="App">
      <script src="https://unpkg.com/react/umd/react.production.min.js" crossorigin></script>

<script
  src="https://unpkg.com/react-dom/umd/react-dom.production.min.js"
  crossorigin></script>

<script
  src="https://unpkg.com/react-bootstrap@next/dist/react-bootstrap.min.js"
  crossorigin></script>

<script>var Alert = ReactBootstrap.Alert;</script>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="#home"></Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#about">About</Nav.Link>
              <Nav.Link href="#games">Games</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <h1>Welcome to Animated Learning!</h1>
        <form onSubmit={submit}>
        <div className="InputFields" style={divStyle}>
        {/* <h2>Enter the Class Recording!</h2> */}
        <input type="text"
        className='recipient_name'
        placeholder="Enter Recording URL"
        onChange={(e)=>setName(e.target.value)}
        // aria-label="Recipient's username"
        aria-describedby="basic-addon2"/>
        
          <div className="AIoptions">
            <label class="container1" id="summary" onChange={(e)=>setSummary(e.target.checked)}>  Summarize
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container1" id="quiz" onChange={(e)=>setQuiz(e.target.checked)}>  Generate Quiz
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container1" id="dates" onChange={(e)=>setDates(e.target.checked)}>  Date Selection
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container1" id="simple" onChange={(e)=>setSimple(e.target.checked)}>  Make it simple
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container1" id="similar" onChange={(e)=>setSimilar(e.target.checked)}>  Topic Change
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            < select
              onChange={e => handleTopicTypeChange(e)}
              disabled={!similar}
              className="browser-default custom-select" >
              {
                Add.map((topic, key) => <option value={key}>{topic}</option>)
              }
            </select >
            {/* <select disabled={!similar}>
              {items.map(item => (
                <option
                  key={item.value}
                  value={item.value}
                  onChange={e=> setTopic(e.target.value)}>
                  {item.label}
                </option>
              ))}
            </select> */}
            {/* <DropdownButton id="dropdown-basic" title="Select Topic" variant="warning" disabled={!similar}>
              <Dropdown.Item href="#/action-1" onChange={(e)=>setTopic(e.target.value)}>Basketball</Dropdown.Item>
              <Dropdown.Item href="#/action-2" onChange={(e)=>setTopic(e.target.value)}>Soccer</Dropdown.Item>
              <Dropdown.Item href="#/action-3" onChange={(e)=>setTopic(e.target.value)}>Tiktok</Dropdown.Item>
              <Dropdown.Item href="#/action-4" onChange={(e)=>setTopic(e.target.value)}>YouTube</Dropdown.Item>
            </DropdownButton> */}

          </div>
          <div className="options">
            <label class="container" id="moana" onChange={(e)=>setMoana(e.target.checked)}><img src={moanaImg} alt="Moana" className="moana"/>
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container" id="rapunzel" onChange={(e)=>setRapunzel(e.target.checked)}><img src={rapunzelImg} alt="Rapunzel"/>
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
            <label class="container" id="shrek" onChange={(e)=>setShrek(e.target.checked)}><img src={shrekImg} alt="Shrek" className="shrek"/>
              <input type="checkbox" />
              <span class="checkmark"></span>
            </label>
          </div>
          <button className='convert_button' type="submit">Convert</button>
          {loading && <p>Processing...</p>}
        </div>
        <div>

        {/* <div className="video" style={{float: 'left'}}>
        {video &&  <iframe width="50%" height="100%" src="https://storage.googleapis.com/audio-files-zoom/generatedWithAudio.mp4"></iframe>}
        </div> */}

        {result && <div>
          
          <div className="container_box">
            <div className="box">
            <h2>Video</h2>
            {video &&  <iframe width="50%" height="80%" src={link}></iframe>}
            </div>
            {summary && <div className="box"> 
             <h2>Summary</h2>
             <p>{sumText}</p>
            </div>}
          </div>


          <div className="container_box">
          { simple &&  <div className="box">
           <h2>Simplified Information</h2>
             <p>{simpText}</p> 
            </div>}
            { dates && <div className="box">
             <h2>Important Dates</h2>
             {sched.map(datesimp => (
               <li>{datesimp}</li>
             ))}
            {/* <p>{sched}</p>  */}
            </div> }
          </div>

          <div className="container_box">
          { quiz &&  <div className="box">
           <h2>Quiz</h2>
            {ques.map((questions, index) => (
                <li>{questions} 
                  <div>
                    { showResults ? <li>{ans[index]}</li> : null }
                  </div>
                </li>
            ))}
            <input type="submit" value="Show Results" onClick={onClick} />
            </div>}
              <div className="box">
                <h2>Checkbook</h2>
                <form>
                  <input type="text" placeholder="Name" onChange={(e)=>setCheckbookName(e.target.value)}/><br/><br/>
                  <input type="text" placeholder="Recepient" onChange={(e)=>setCheckbookRecepient(e.target.value)}/><br/><br/>
                  <input type="text" placeholder="Amount" onChange={(e)=>setCheckbookAmount(e.target.value)}/><br/><br/>
                  <input type="text" placeholder="Description" onChange={(e)=>setCheckbookDesc(e.target.value)}/><br/><br/>
                  <input type="submit" value="Submit" onClick={checkbook} />
                </form>
                {ischeckbook && <a href={chechbookimg} target="_blank">Click here to see the generated Check URI</a>}
              </div>
            </div>

            <div className="container_box">
            <div className="box">
              <h2>Transcript</h2>
              <p>{transcript}</p>
              </div>
             {similar && <div className="box">
              <h2>Similarly</h2>
              <p>{similar}</p>
              </div>}
          </div>

          </div>}
        </div>
        {/* {result && } */}
        </form>
        {/* <Teacher /> */}
    </div>
  );
}

export default App;
