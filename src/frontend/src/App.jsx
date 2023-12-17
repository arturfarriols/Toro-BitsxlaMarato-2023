import Header from './components/Header';
import Footer from './components/Footer';
import FileUploadComponent from './components/FileUploadComponent';
import './App.css'

function App() {

  return (
    <>
    <div className='bg-neutral-100'>
      <Header />
      <FileUploadComponent />
      <Footer />
      </div>
    </>
  )
}

export default App
