dcup:
	docker compose up -d && ${MAKE} dclogs
dcstop:
	docker compose stop
dclogs:
	docker compose logs -f
dcbash:
	docker compose exec -it app bash
dcrm:
	docker compose rm -f -s app
dprune:
	docker system prune -a -f
dctest:
	docker compose exec -it app bash -c 'pytest'