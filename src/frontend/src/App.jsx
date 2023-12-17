import Header from './components/Header';
import Footer from './components/Footer';
import FileUploadComponent from './components/FileUploadComponent';
import FileList from './components/ImageUploader';
import './App.css'

function App() {

  return (
    <>
    <div className='bg-neutral-100'>
      <Header />
      <FileList />
      <Footer />
      </div>
    </>
  )
}

export default App
