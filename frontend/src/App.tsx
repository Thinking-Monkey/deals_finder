import 'react'
import Header from './components/Header'
import Card from './components/Card'
import Button from './components/Button'
import DropDownButton from './components/DropDownButton'

export default function App(){
   return (
    <>
      <Header />
      <Button title="LOAD MORE" />
      <DropDownButton title="NONE" />
      <Card 
        title="Deus Ex: Human Revolution"
        subTitle="Director's Cut"
        imgUrl='https://cdn.cloudflare.steamstatic.com/steam/apps/238010/capsule_sm_120.jpg?t=1619788192'
        alt='Sample Image'
        color='bg-red-600'
        price={35}
        dealPrice={15}
        isLogged={false}
      />
    </>
  )
}