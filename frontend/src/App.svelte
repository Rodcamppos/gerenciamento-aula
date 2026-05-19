<script>
  import { onMount } from 'svelte';

  let planos = [];
  let loading = true;
  let loadingIA = false;
  let erro = null;

  let novoPlano = {
    titulo: '',
    disciplina: '',
    ementa: '',
    objetivo: '',
    data_prevista: '',
    conteudos: '',
    recursos_apoio: '',
    tags: ''
  };

  async function carregarPlanos() {
    try {
      loading = true;
      const res = await fetch('http://localhost:5000/api/planos');
      if (!res.ok) throw new Error();
      const data = await res.json();
      planos = data.planos;
    } catch (e) {
      erro = "Erro ao conectar com a API.";
    } finally {
      loading = false;
    }
  }

  async function consultarIA() {
    if (!novoPlano.titulo || !novoPlano.ementa) {
      alert("Preencha título e ementa.");
      return;
    }

    try {
      loadingIA = true;
      const res = await fetch('http://localhost:5000/api/ia/recomendar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          titulo: novoPlano.titulo,
          disciplina: novoPlano.disciplina,
          ementa: novoPlano.ementa
        })
      });
      
      const sugestao = await res.json();
      
      if (res.ok) {
        novoPlano.conteudos = sugestao.conteudos || '';
        novoPlano.tags = Array.isArray(sugestao.tags) ? sugestao.tags.join(', ') : (sugestao.tags || '');
      } else {
        alert("Erro retornado pela IA: " + (sugestao.error || "Erro desconhecido"));
      }
    } catch (e) {
      alert("Erro na conexão com a IA.");
    } finally {
      loadingIA = false;
    }
  }

  async function salvarPlano() {
    try {
      const res = await fetch('http://localhost:5000/api/planos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novoPlano)
      });
      
      const data = await res.json();
      
      if (res.ok) {
        alert("Plano salvo com sucesso!");
        novoPlano = { titulo: '', disciplina: '', ementa: '', objetivo: '', data_prevista: '', conteudos: '', recursos_apoio: '', tags: '' };
        carregarPlanos();
      } else {
        console.error("Detalhes do erro 400:", data);
        alert("Erro de validação nos campos: " + JSON.stringify(data));
      }
    } catch (e) {
      alert("Erro ao conectar com o servidor para salvar.");
    }
  }

  onMount(carregarPlanos);
</script>

<main>
  <header>
    <h1>Gerenciador de Aulas</h1>
  </header>

  <section class="editor">
    <div class="field-group">
      <input bind:value={novoPlano.titulo} placeholder="Título da Aula" />
      <input bind:value={novoPlano.disciplina} placeholder="Disciplina" />
      <input type="date" bind:value={novoPlano.data_prevista} />
    </div>

    <textarea bind:value={novoPlano.ementa} placeholder="Ementa"></textarea>
    <textarea bind:value={novoPlano.objetivo} placeholder="Objetivo"></textarea>

    <div class="ai-box">
      <button class="btn-ia" on:click={consultarIA} disabled={loadingIA}>
        {loadingIA ? 'Processando...' : 'Smart Assist'}
      </button>
      
      <textarea bind:value={novoPlano.conteudos} placeholder="Conteúdos Sugeridos"></textarea>
      <input bind:value={novoPlano.tags} placeholder="Tags geradas" />
    </div>

    <button class="btn-save" on:click={salvarPlano}>Salvar Plano</button>
  </section>

  <section class="list">
    {#if loading}
      <p>Carregando...</p>
    {:else if erro}
      <p class="error">{erro}</p>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Disciplina</th>
            <th>Data</th>
          </tr>
        </thead>
        <tbody>
          {#each planos as plano}
            <tr>
              <td>{plano.titulo}</td>
              <td>{plano.disciplina}</td>
              <td>{plano.data_prevista || 'Não informada'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>
</main>

<style>
  :global(body) { background: #f4f7f6; font-family: system-ui; }
  main { max-width: 900px; margin: 0 auto; padding: 2rem; }
  section { background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
  .field-group { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px; margin-bottom: 10px; }
  input, textarea { width: 100%; padding: 12px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
  textarea { height: 80px; resize: vertical; }
  .ai-box { background: #eef2ff; padding: 15px; border-radius: 6px; margin: 10px 0; border-left: 4px solid #4f46e5; }
  button { padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
  .btn-ia { background: #4f46e5; color: white; margin-bottom: 10px; }
  .btn-save { background: #10b981; color: white; width: 100%; font-size: 1.1rem; }
  table { width: 100%; border-collapse: collapse; }
  th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }
  th { background: #fafafa; }
  .error { color: red; }
</style>