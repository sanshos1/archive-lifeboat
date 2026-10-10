import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as contract_actions
def compat(method=None,args=None,kwargs=None):
 out={}
 if method is not None: out['method']=method
 if args: out['args']=args
 if kwargs: out['kwargs']=kwargs
 return out
contract_actions.make_calldata_object=compat
ROOT=Path(__file__).parents[1]; ENV=(ROOT.parents[3]/'accounts.env').read_text(); ADDRESS=json.loads((ROOT/'deployment.json').read_text())['contractAddress']; KEY=re.search(r'^ACCOUNT_3_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip(); c=create_client(chain=studionet,account=create_account(account_private_key=KEY)); stranger=create_client(chain=studionet,account=create_account())
def wait(client,tx,expect='SUCCESS'):
 r=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True); leaders=r.get('consensus_data',{}).get('leader_receipt') or []; leaders=[leaders] if isinstance(leaders,dict) else leaders; ex=[str(x.get('execution_result','')).upper() for x in leaders]; assert r.get('result_name')=='MAJORITY_AGREE' and expect in ex; return r,ex
def write(client,name,args):
 tx=client.write_contract(address=ADDRESS,function_name=name,args=args); print(name+'_tx='+str(tx),flush=True); wait(client,tx); return str(tx)
cid='LIFEBOAT-'+str(int(time.time())); base='https://raw.githubusercontent.com/sanshos1/archive-lifeboat/main/fixtures/'; tx={'launch':write(c,'launch',[cid,'Lantern Index preservation set',base+'origin.txt',base+'mirror-a.txt',base+'mirror-b.txt',base+'policy.txt'])}; launched=c.read_contract(address=ADDRESS,function_name='get_capsule',args=[cid]); assert launched['state']=='AFLOAT'; tx['inspect']=write(c,'inspect',[cid]); inspected=c.read_contract(address=ADDRESS,function_name='get_capsule',args=[cid]); assert inspected['state']=='INSPECTED'; bad=stranger.write_contract(address=ADDRESS,function_name='seal',args=[cid]); tx['unauthorizedSeal']=str(bad); br,be=wait(stranger,bad,'ERROR'); assert c.read_contract(address=ADDRESS,function_name='get_capsule',args=[cid])['state']=='INSPECTED'; tx['seal']=write(c,'seal',[cid]); final=c.read_contract(address=ADDRESS,function_name='get_capsule',args=[cid]); assert final['state']=='SEALED'; proof={'capsuleId':cid,'contract':ADDRESS,'transactions':tx,'launched':launched,'inspected':inspected,'final':final,'unauthorizedSeal':{'consensus':br.get('result_name'),'execution':be},'fixtureDisclosure':'Public fixtures demonstrate four-source digest freezing, fidelity consensus, owner-only sealing, and state preservation after an unauthorized call.'}; (ROOT/'evidence'/'live-run.json').write_text(json.dumps(proof,indent=2)+'\n'); print(json.dumps(proof,indent=2))
