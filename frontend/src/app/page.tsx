import Link from "next/link";
import { CompletionFlower, Wordmark } from "@/components/ui";

const tools = [
  ["01", "Perspective Lens", "One story. More than one angle.", "Compare how publishers cover an event, with sources you can open yourself.", "lavender"],
  ["02", "Time Machine", "There’s always a before.", "Trace the events and coverage that brought a story to this moment.", "yellow"],
  ["03", "Connection Explorer", "Find the thread between things.", "Explore a knowledge graph of related stories and the evidence connecting them.", "mint"],
  ["04", "Knowledge Passport", "Keep the things that clicked.", "Save your explorations and revisit the concepts you’ve discovered. No streaks to keep up with.", "peach"],
];

export default function Home() {
  return <div className="landing">
    <header className="landing-nav">
      <Link href="/" aria-label="Finite home"><Wordmark /></Link>
      <nav aria-label="Website navigation"><a href="#how-it-works" className="landing-about">How it works</a><Link href="/login">Log in</Link><Link href="/signup" className="landing-button">Get started <span aria-hidden="true">↗</span></Link></nav>
    </header>
    <main>
      <section className="landing-hero rise">
        <div className="landing-intro">
          <p className="landing-kicker">FOR CURIOUS MINDS. AND FULL LIVES.</p>
          <h1>Less scrolling.<br /><em>More understanding.</em></h1>
          <p className="landing-description">A personal news briefing with room to wonder. Find out what happened, follow the questions that matter to you, and reach a place to stop.</p>
          <div className="landing-actions"><Link href="/signup" className="landing-button">Make room for curiosity <span aria-hidden="true">↗</span></Link><a href="#how-it-works">Take a little look <span aria-hidden="true">↓</span></a></div>
          <p className="landing-footnote">A finite feed. Source-backed exploration. A proper ending.</p>
        </div>
        <div className="landing-preview" aria-label="Illustration of the Finite journey">
          <div className="landing-preview-label">A LITTLE TOUR OF FINITE</div>
          <article className="landing-paper"><span className="landing-kicker">01 / YOUR DAILY BRIEFING</span><h2>The world,<br />in a few stories.</h2><div className="landing-paper-lines" aria-hidden="true"><i /><i /><i /></div><span className="landing-tag">Chosen around your interests</span></article>
          <div className="landing-question"><span aria-hidden="true">↳</span> But how did we get here?</div>
          <div className="landing-ending"><CompletionFlower /><div><strong>Curiosity, satisfied.</strong><p>Now, back to your day.</p></div></div>
        </div>
      </section>
      <section id="how-it-works" className="landing-section">
        <div className="landing-section-heading"><p className="landing-kicker">A SMALL RITUAL, NOT AN ENDLESS FEED</p><h2>Catch up. Dig a little deeper.<br /><em>Then close the tab.</em></h2></div>
        <div className="landing-steps">
          <article><span>01</span><h3>Make it yours.</h3><p>Choose your interests, reading depth and briefing size. Read in English, with Malayalam support too.</p></article>
          <article><span>02</span><h3>Follow a question.</h3><p>Go beyond the headline into context, history and connections. Each exploration has sources and a limit.</p></article>
          <article><span>03</span><h3>Leave with something.</h3><p>Save what you explored to your Passport. Your briefing ends. There’s no next page waiting for you.</p></article>
        </div>
      </section>
      <section className="landing-section" aria-labelledby="tools-heading">
        <div className="landing-section-heading"><p className="landing-kicker">A FEW WAYS TO GO “OH, NOW I GET IT.”</p><h2 id="tools-heading">Give your curiosity<br /><em>somewhere to play.</em></h2></div>
        <div className="landing-tools">{tools.map(([number, name, title, description, color]) => <article key={name} className={`landing-tool ${color}`}><div className="landing-tool-top"><span>{name}</span><span aria-hidden="true">{number}</span></div><h3>{title}</h3><p>{description}</p></article>)}</div>
      </section>
      <section className="landing-finish"><CompletionFlower /><p className="landing-kicker">NEWS THAT ENDS. UNDERSTANDING THAT DOESN’T.</p><h2>The world is a lot.<br /><em>Your news doesn’t have to be.</em></h2><Link href="/signup" className="landing-button">Create your account <span aria-hidden="true">↗</span></Link><p>Already have an account? <Link href="/start">Open your briefing →</Link></p></section>
    </main>
    <footer className="landing-footer"><Link href="/" aria-label="Finite home"><Wordmark /></Link><p>Stay curious. Then carry on.</p><Link href="/login">Log in ↗</Link></footer>
  </div>;
}
